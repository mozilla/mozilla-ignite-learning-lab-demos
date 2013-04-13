# Copyright 2012 James McCauley, Kenny Katzgrau
#
# This is an example component to be used with the
# Mozilla Ignite SDN Learning Labs.  
# 
# It demonstrates fine-grained control over packet handling
# available with OpenFlow. This is intended as an experiment
# for the purposes of learning, and not as something you
# would want to try in a production environment

"""
This is a POX component that turns a switch into a TCP-based load
balancer. Any hosts connected to the openflow ports are expected
to be webservers listening on port 8000.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr

log = core.getLogger()

class LoadBalancer(object):
  """
  Load Balancer

  1. Respond to ARP requests looking for 192.168.0.200
     This is a fake address, but it will act as our virtual
     load balancer's address
  2. Look for TCP packets headed to 192.168.0.200:80 with 
     the SYN flag set (start of TCP transmission)
  4. Keep track of source address and port of the TCP packet
     Anything in the future with the destination address
     and port matching the stored source address and port
     should be rewritten to have the source as 192.168.0.200:80
  5. Rewrite the packet so it heads to a randomly-selected
     host attached to an OpenFlow port
     Rewrite:
      - IP address
      - MAC address
      - UDP port - 8000 (where our webservers will listen)
  6. Look for FIN-flagged packets headed from a Webserver host. 
     After the packet is rewritten, remove the stored entry in 
     our connections

  Note: If there are no hosts hooked up, send back an HTTP 503
  signifying that there are no upstream servers.

  This is a proof-of-concept. 
  There's definitely room for improvement!
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Keep track of TCP connections ip: {}
    self.macs = {}

    log.debug('Starting load balancer ..')

  def reroute(self, event, new_addr):
      # The goal here is to take the contents of the original
      # UDP packet and modify them. When then need to package
      # It up in an enclosing IP packet
      # And finally, enclose it in an Ethernet packet
      packet = event.parsed
      packet.src = packet.dst # router is the dst
      packet.dst = EthAddr('00:11:11:AF:5E:E6')
      packet.payload.srcip = packet.payload.dstip
      packet.payload.dstip = IPAddr(new_addr)

      # Now let's encapsulate all this in a special message that
      #  will be sent back to our router. The instruction here
      #  for the switch is to forward the packet we created on
      #  all of the router/switch's physical ports
      msg = of.ofp_packet_out()
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      msg.data = packet.pack()

      # Send it along
      event.connection.send(msg)

      # Log some data describing what just happened
      log.debug("Sent a TCP packet to %s:%s from %s:%s", packet.payload.dstip, packet.payload.payload.dstport, packet.payload.srcip, packet.payload.payload.srcport)

  def _handle_PacketIn (self, event):
    packet = event.parsed

    # Hold on to the original TCP packet we received
    old_ip  = packet.find("ipv4")
    old_udp = packet.find("udp")
    old_tcp = packet.find("tcp")

    if old_ip:
      log.debug('Saw IP packet headed to %s from %s', old_ip.dstip, old_ip.srcip);

    if old_tcp:
      if old_tcp.dstport == 8000:
        log.debug('TCP *TO* port 8000')
        self.reroute(event, '192.168.1.100')
        return
      if old_tcp.srcport == 8000:
        log.debug('TCP *FROM* port 8000')
        self.reroute(event, '192.168.1.100')
        return

    # Check for some conditions
    # In our Mozilla experiment, we send UDP packets on port 10002
    # so we look for those
    if old_udp and old_udp.dstport == 10002:
      pass
    else:
      # In the event we received some packet we don't care about,
      #  send it to along to where it was headed on all physical ports
      msg = of.ofp_packet_out()
      # A bit of a shortcode. Here we're just jamming the old
      #  packet data into a message for the switch. We don't
      #  need to construct a new packet like we did before
      msg.data = event.ofp
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      # Send the instruction to switch
      self.connection.send(msg)

# This method is called for all controller components in POX
#  on initialization
def launch ():
  # Start the DHCP server (for assigning IP addresses)
  from misc.dhcpd import default
  default()

  # Add keepalive to avoid connection drops
  from openflow.keepalive import launch
  launch()

  # Add basic switch functionality
  #from forwarding.l3_learning import launch
  #launch()

  # Respond to ARP requests
  from misc.arp_responder import launch
  launch()

  # This is a handler that will be called when the switch connects
  #  to this controller
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    # We want the entire body of the packet
    core.openflow.miss_send_len = 0xffff
    # Create in instance of our load balancer
    LoadBalancer(event.connection)

  # Tell POX to use the above handler when the switch connection
  #  is alive
  core.openflow.addListenerByName("ConnectionUp", start_switch)
