from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
import pox.lib.packet as pkt
import json

from .constants import RULES_PATH
from .rules.Rule1 import Rule1
from .rules.Rule2 import Rule2
from .rules.Rule3 import Rule3


class Firewall(EventMixin):
    def __init__(self, firewall_switch_id):
        self.listenTo(core.openflow)
        self.rules = self._init_rules()
        self._parse_configuration(RULES_PATH)
        self.firewall_switch_id = firewall_switch_id


    def _parse_configuration(self, json_path):
        with open(json_path, "r") as f:
            rules_json = json.load(f)
            self.rules[1].set_is_activated(rules_json["r1_enabled"])
            self.rules[2].set_is_activated(rules_json["r2_enabled"])
            self.rules[3].set_is_activated(rules_json["r3_enabled"])
            self.rules[2].set_host(rules_json["r2_blocked_host"])
            self.rules[3].set_ips_to_block(rules_json["r3_first_blocked"], rules_json["r3_second_blocked"])


    def  _handle_ConnectionUp(self, event):
        pass



    def rule_applies(self, packet):
        for rule in self.rules.values():
            if rule.is_activated() and rule.evaluate(packet):
                return True

        return False


    def _init_rules(self):
        return {
            1: Rule1(),
            2: Rule2(),
            3: Rule3()
        }
