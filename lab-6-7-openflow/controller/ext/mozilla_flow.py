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
This is a POX component that installs a flow on an OpenFlow
enabled router. When the OpenFlow connection is fired up,
is installs a flow on the switch that will take any packets
headed to port 10002 and send them to port 10003 instead.

Check out Flow.installRedirectFlow to see how that's done
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
#from pox.lib.addresses import EthAddr

log = core.getLogger()

class Flow(object):
  """
  This class shows how you can install flows
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    self.installRedirectFlow()

  def installRedirectFlow (self):
    """
    Install a flow directing UDP packets headed to port 10002 to go
    to 10003 instead.
    """
    log.debug('Installing 10002 -> 10003')
    msg = of.ofp_flow_mod()
    msg.priority = 100

    # Note the line starting with 'msg.match' - that's the line where
    # we're telling the router which kind of packets should be 
    # guided by this rule.
    msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.UDP_PROTOCOL, tp_dst = 10002)
    # Now we'll set what kind of things should happen with
    # packets that match the rule above
    msg.actions.append(of.ofp_action_tp_port.set_dst(10003))
    msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
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
  from forwarding.l2_learning import launch
  launch()

  # This is a handler that will be called when the switch connects
  #  to this controller
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    # Create in instance of our Flow creator, and pass
    #  it the switch connection so we can add handlers
    #  when packets come in
    # Add basic switch functionality
    Flow(event.connection)

  # Tell POX to use the above handler when the switch connection
  #  is alive
  core.openflow.addListenerByName("ConnectionUp", start_switch)
