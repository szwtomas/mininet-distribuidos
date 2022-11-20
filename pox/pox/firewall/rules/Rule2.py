from .Rule import Rule
from ..constants import DROP_PORT
from pox.lib.packet.ipv4 import ipv4
from ..utils import is_udp_or_tcp, log_rule_block

class Rule2(Rule, object):
    def __init__(self, host=""):
        super(Rule2, self).__init__()
        self.host = host


    def set_host(self, host):
        self.host = host


    def evaluate(self, link_packet):
        # src is host 1, dst port is 5001 and protocol is UDP
        ip_packet = link_packet.payload

        if not is_udp_or_tcp(ip_packet.protocol):
            return False

        if ip_packet.srcip != self.host:
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == DROP_PORT and ip_packet.protocol == ipv4.UDP_PROTOCOL:
            log_rule_block(2, ip_packet.srcip, ip_packet.dstip)
            return True

        return False