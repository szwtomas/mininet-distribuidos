from pox.core import core
from pox.lib.revent import *
import json
from .constants import RULES_PATH
from .rules.Rule1 import Rule1
from .rules.Rule2 import Rule2
from .rules.Rule3 import Rule3

log = core.getLogger()

class Firewall:
    def __init__(self, firewall_switch):
        self.firewall_switch = firewall_switch
        self.rules = self._init_rules()
        self._parse_configuration(RULES_PATH)

    def start(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        if int(self.firewall_switch) == event.dpid:
            log.info("Firewall set into switch: {}".format(self.firewall_switch))
            for rule in self.rules.values():
                if rule.is_activated():
                    rule.add_table_rule(event)

    def _parse_configuration(self, json_path):
        with open(json_path, "r") as f:
            rules_json = json.load(f)
            self.rules[1].set_is_activated(rules_json["r1_enabled"])
            self.rules[2].set_is_activated(rules_json["r2_enabled"])
            self.rules[3].set_is_activated(rules_json["r3_enabled"])
            self.rules[2].set_host(rules_json["r2_blocked_host"])
            self.rules[3].set_ips_to_block(rules_json["r3_first_blocked"], rules_json["r3_second_blocked"])

    def _init_rules(self):
        return {
            1: Rule1(),
            2: Rule2(),
            3: Rule3()
        }

def launch(firewall_switch):
    firewall = Firewall(firewall_switch)
    firewall.start()
