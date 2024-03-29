from pox.core import core
from ..constants import DROP_PORT
from .Rule import Rule
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr

log = core.getLogger()

class Rule2(Rule):
    def __init__(self):
        self.host = ''


    def set_host(self, host):
        self.host = host


    def add_table_rule(self, event):
        # block packets with dst port 5001, src is host 1 and protocol is UDP
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.nw_proto = pkt.ipv4.UDP_PROTOCOL
        match.tp_dst = DROP_PORT
        match.nw_src = IPAddr(self.host)

        self._send_packet(event, match)
        log.info("Rule 2 applied")
