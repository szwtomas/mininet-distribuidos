from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.packet.ethernet import ethernet
import json
from .constants import RULES_PATH
from .rules import Rule1, Rule2, Rule3

firewall_switch_id = None

class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.rules = self._init_rules()        
        self._parse_configuration(RULES_PATH)


    def _parse_configuration(self, json_path):
        with open(json_path, "r") as f:
            rules_json = json.load(f)
            self.rules[1].set_is_activated(rules_json["r1_enabled"])
            self.rules[2].set_is_activated(rules_json["r2_enabled"])
            self.rules[3].set_is_activated(rules_json["r3_enabled"])
            self.rules[2].set_host(rules_json["r2_blocked_host"])
            self.rules[3].set_ips_to_block(rules_json["r3_first_blocked"], rules_json["r3_second_blocked"])


    def _handle_PacketIn(self, event):
        packet = event.parsed
        print(packet)

        # Ignore Ip packet
        if packet.type != ethernet.IP_TYPE:
            return

        if self.rule_applies(packet):
            msg = of.ofp_flow_mod()
            match = of.ofp_match.from_packet(packet)
            msg.match = match
            event.connection.send(msg)
            event.halt = True


    def rule_applies(self, packet):
        for rule in self.rules:
            if rule.is_activated() and rule.verify(packet):
                return True

        return False


    def _init_rules(self):
        return {
            1: Rule1(),
            2: Rule2(),
            3: Rule3()
        }

