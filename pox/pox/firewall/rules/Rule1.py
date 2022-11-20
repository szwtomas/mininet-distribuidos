from .Rule import Rule
from ..constants import HTTP_PORT
from ..utils import is_udp_or_tcp, log_rule_block

class Rule1(Rule):

    def __init__(self):
        super().__init__()

    def evaluate(self, link_packet):
        ip_packet = link_packet.payload

        if not is_udp_or_tcp(ip_packet.protocol):
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == HTTP_PORT:
            log_rule_block(1, ip_packet.srcip, ip_packet.dstip)
            return True

        return False
