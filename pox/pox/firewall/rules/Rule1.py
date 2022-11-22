from pox.core import core
from .Rule import Rule
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from ..constants import HTTP_PORT


log = core.getLogger()

class Rule1(Rule):
    def __init__(self):
        pass

    def add_table_rule(self, event):
        # block packets with dst port 80
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        match.tp_dst = HTTP_PORT

        self._send_packet(event, match)
        log.info("Rule 1 applied")
