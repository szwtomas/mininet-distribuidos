import pox.forwarding.l2_learning as fw
import pox.openflow.libopenflow_01 as of

from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.ethernet import ethernet

from pox.core import core

log = core.getLogger()


class Controller:
    def __init__(self, test):
        print(test)

    def start(self):
        print("starting")
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        print("handle_connection_up:", event)
    
    def _handle_PacketIn(self, event):
        eth_packet = event.parsed
        if eth_packet.type != ethernet.IP_TYPE:
            return
        print("handle_packet_in: ", eth_packet)

def launch(test):
    fw.launch()

    controller = Controller(test)
    core.call_when_ready(controller.start(), "openflow")
