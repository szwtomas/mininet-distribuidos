from pox.core import core
from pox.lib.packet.ipv4 import ipv4

log = core.getLogger() 

def is_udp_or_tcp(protocol):
    return protocol in (ipv4.TCP_PROTOCOL, ipv4.UDP_PROTOCOL)


def log_rule_block(rule_number, srcip, dstip):
    log_message = "Rule " + str(rule_number) + ": Blocking a flow from " + str(srcip) + " to " + str(dstip) 
    log.info(log_message)
