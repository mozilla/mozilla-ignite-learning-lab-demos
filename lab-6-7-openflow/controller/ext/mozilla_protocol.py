# Copyright 2012 James McCauley, Kenny Katzgrau
#
# This is an example component to be used with the
# Mozilla Ignite SDN Learning Labs.  
# 
# This is a contrived example demonstrating 
# how a new "protocol" could be written and
# handled appropriately by a switch

"""
This is a POX component that turns a switch into a hub,
and additionally modifies the contents of UDP packets
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import re
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr

log = core.getLogger()

class Proto(object):

  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Send all packets here
    fm = of.ofp_flow_mod()
    fm.priority = 0x7000 # Pretty high
    fm.match.dl_type = 0x0800
    fm.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    connection.send(fm)

  def sendPacket(self, event, new_addr):
    dpid    = event.connection.dpid
    ipEth   = core.learning_switch.arpTable[dpid]
    packet  = event.parsed
    old_udp = packet.find('udp')

    # The goal here is to take the contents of the original
    # UDP packet and modify them. When then need to package
    # It up in an enclosing IP packet
    # And finally, enclose it in an Ethernet packet
    new_addr = IPAddr(new_addr)
    #log.debug('Sent packet to: %s', new_addr)
    #log.debug(ipEth)

    if new_addr in ipEth:
      packet.dst = ipEth[new_addr]
      packet.payload.dstip = new_addr
      log.debug('Sending SUPERCAST from %s to %s: %s', packet.payload.srcip, new_addr, old_udp.payload)

      new_udp         = pkt.udp()
      new_udp.srcport = old_udp.srcport
      new_udp.dstport = old_udp.dstport
      new_udp.payload = old_udp.payload

      # Create new new IP packet to enclose the UDP
      # packet we just created. The line that says new_ip.payload = new_udp
      # is where that happens
      new_ip = pkt.ipv4()
      new_ip.protocol = new_ip.UDP_PROTOCOL
      new_ip.srcip    = packet.find("ipv4").srcip
      new_ip.dstip    = new_addr
      new_ip.payload  = new_udp

      # And like before, enclose the IP packet in an ethernet packet
      new_eth         = pkt.ethernet()
      new_eth.src     = packet.src
      new_eth.dst     = ipEth[new_addr].mac
      new_eth.type    = new_eth.IP_TYPE
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

    else:
      log.debug('Saw a SUPERCAST packet with %s as a recipient, but unknown MAC', new_addr)
      # Now let's encapsulate all this in a special message that
      #  will be sent back to our router. The instruction here
      #  for the switch is to forward the packet we created on
      #  all of the router/switch's physical ports
      msg = of.ofp_packet_out()
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      msg.data = event.ofp

      # Send it along
      event.connection.send(msg)

  def _handle_PacketIn (self, event):
    packet = event.parsed
    # Hold on to the original UDP packet we received
    udp = packet.find("udp")
    # Check for some conditions
    # 1. It's a UDP packet
    # 2. It has the SUPERCAST header
    # 3. It has a list of IP addresses after the header

    # This will be our match object
    m = False
    if udp:
      # OK, it's a UDP packet
      m = re.findall('(SUPERCAST)', str(udp.payload))
      if m:
        # Nice, it has the SUPERCAST header
        ips = re.findall('\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}', str(udp.payload))
        # Now, let's remove the supercast header
        pieces = udp.payload.split('\n\n')
        if len(pieces) > 1:
          udp.payload = "\n\n".join(pieces[1:])
        # Now run through the IPs listed and send the packet out
        if ips:
          log.debug('SUPERCAST request to %s', ips)
          for ip in ips:
            self.sendPacket(event, ip)
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
  from forwarding.l3_learning import launch
  launch()

  # This is a handler that will be called when the switch connects
  #  to this controller
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    # We want the entire body of the packet
    core.openflow.miss_send_len = 0xffff
    # Create in instance of our protocol handler, and pass
    #  it the switch connection so we can add handlers
    #  when packets come in
    Proto(event.connection)

  # Tell POX to use the above handler when the switch connection
  #  is alive
  core.openflow.addListenerByName("ConnectionUp", start_switch)
