import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

class Rule():
    def __init__(self, is_activated=False):
        self._is_activated = is_activated

    def is_activated(self):
        return self._is_activated

    def set_is_activated(self, activated):
        self._is_activated = activated

    def _send_packet(self, event, match):
        msg = of.ofp_flow_mod()
        msg.match = match
        event.connection.send(msg)

    def add_table_rule(self, event):
        pass
