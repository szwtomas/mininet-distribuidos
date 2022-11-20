from .Rule import Rule
from ..utils import log_rule_block

class Rule3(Rule):

    def __init__(self, ip_blocked1="", ip_blocked2=""):
        super().__init__()
        self.ip_blocked1 = ip_blocked1
        self.ip_blocked2 = ip_blocked2


    def evaluate(self, link_packet):
        ip_packet = link_packet.payload
        if self._should_block_packet(ip_packet):    
            log_rule_block(3, ip_packet.srcip, ip_packet.dstip)
            return True
        return False


    def set_ips_to_block(self, ip1, ip2):
        self.ip_blocked1 = ip1
        self.ip_blocked2 = ip2
        

    def _should_block_packet(self, ip_packet):
        is_blocked_2 = ip_packet.srcip == self.ip_blocked2 and ip_packet.dstip == self.ip_blocked1
        is_blocked_1 = ip_packet.srcip == self.ip_blocked1 and ip_packet.dstip == self.ip_blocked2 
        return is_blocked_1 or is_blocked_2




