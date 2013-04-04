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
This is a POX component that turns a switch into a hub,
and additionally modifies the contents of UDP packets
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
#from pox.lib.addresses import EthAddr

log = core.getLogger()

class Injector(object):
  """
  This class provides the functionality for both modifying packets
  and additionally, turning a switch into a hub
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def _handle_PacketIn (self, event):
    packet = event.parsed

    # Hold on to the original UDP packet we received
    old_udp = packet.find("udp")

    # Check for some conditions
    # In our Mozilla experiment, we send UDP packets on port 10002
    # so we look for those
    if old_udp and old_udp.dstport == 10002:
      # The goal here is to take the contents of the original
      # UDP packet and modify them. When then need to package
      # It up in an enclosing IP packet
      # And finally, enclose it in an Ethernet packet

      # Create a new packet with the same info as the old
      # - ecept the contents are modified
      new_udp         = pkt.udp()
      new_udp.srcport = old_udp.srcport
      new_udp.dstport = old_udp.dstport
      new_udp.payload = 'Modified with Openflow:' + old_udp.payload

      # Create new new IP packet to enclose the UDP
      # packet we just created. The line that says new_ip.payload = new_udp
      # is where that happens
      new_ip = pkt.ipv4()
      new_ip.protocol = new_ip.UDP_PROTOCOL
      new_ip.srcip = packet.find("ipv4").srcip
      new_ip.dstip = packet.find("ipv4").dstip
      new_ip.payload = new_udp

      # And like before, enclose the IP packet in an ethernet packet
      new_eth = pkt.ethernet()
      new_eth.src = packet.src
      new_eth.dst = packet.dst
      new_eth.type = new_eth.IP_TYPE
      new_eth.payload = new_ip

      # Now let's encapsulate all this in a special message that
      #  will be sent back to our router. The instruction here
      #  for the switch is to forward the packet we created on
      #  all of the router/switch's physical ports
      msg = of.ofp_packet_out()
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      msg.data = new_eth.pack()

      # Send it along
      event.connection.send(msg)

      # Log some data describing what just happened
      log.debug("Sent a modified UDP packet from %s to %s", new_ip.dstip, new_ip.srcip)
      log.debug('Original Payload: ' + old_udp.payload)
      log.debug('New Payload: ' + new_udp.payload)
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

  # This is a handler that will be called when the switch connects
  #  to this controller
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    # We want the entire body of the packet
    core.openflow.miss_send_len = 0xffff
    # Create in instance of our packet injector, and pass
    #  it the switch connection so we can add handlers
    #  when packets come in
    Injector(event.connection)

  # Tell POX to use the above handler when the switch connection
  #  is alive
  core.openflow.addListenerByName("ConnectionUp", start_switch)
