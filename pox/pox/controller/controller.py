from pox.core import core
from firewall.firewall import Firewall
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
log = core.getLogger()


class Controller:
    def __init__(self, firewall_switch):
        self.firewall_switch = firewall_switch

    def start(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        if int(self.firewall_switch) == event.dpid:
            log.info("Firewall set into switch: {}".format(self.firewall_switch))

            match = of.ofp_match()
            # block packets with dst port 80
            match.dl_type = pkt.ethernet.IP_TYPE
            match.nw_proto = pkt.ipv4.TCP_PROTOCOL
            match.tp_dst = 80

            # block packets with dst port 5001, src is host 1 and protocol is UDP
            match2 = of.ofp_match()
            match2.dl_type = pkt.ethernet.IP_TYPE
            match2.nw_proto = pkt.ipv4.UDP_PROTOCOL
            match2.tp_dst = 5001
            match2.nw_src = IPAddr('10.0.0.1') # host 1

            # Rule 3 could be applied using ips or macs

            # block packets between from host 1 to host 2
            match3 = of.ofp_match()
            match3.dl_type = pkt.ethernet.IP_TYPE
            
            match3.nw_src = IPAddr('10.0.0.1')
            match3.nw_dst = IPAddr('10.0.0.2')

            # block packets between from host 2 to host 1
            match4 = of.ofp_match()
            match4.dl_type = pkt.ethernet.IP_TYPE
            match4.nw_src = IPAddr('10.0.0.2')
            match4.nw_dst = IPAddr('10.0.0.1')

            # send msg
            for rule in [match, match2, match3, match4]:
                msg = of.ofp_flow_mod()
                msg.match = rule
                event.connection.send(msg)




def launch(firewall_switch):
    controller = Controller(firewall_switch)
    controller.start()
