from .Rule import Rule
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr

class Rule3(Rule):
    def __init__(self):
        self.ip_blocked1 = ''
        self.ip_blocked2 = ''

    def add_table_rule(self, event):
        # Rule 3 could be applied using IPs or MACs (we use IPs)
        # block packets between from host 1 to host 2
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.nw_src = IPAddr(self.ip_blocked1)
        match.nw_dst = IPAddr(self.ip_blocked2)

        # block packets between from host 2 to host 1
        match2 = of.ofp_match()
        match2.dl_type = pkt.ethernet.IP_TYPE
        match2.nw_src = IPAddr(self.ip_blocked2)
        match2.nw_dst = IPAddr(self.ip_blocked1)

        self._send_packet(event, match)
        self._send_packet(event, match2)

    def set_ips_to_block(self, ip1, ip2):
        self.ip_blocked1 = ip1
        self.ip_blocked2 = ip2
