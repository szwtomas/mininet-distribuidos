from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
import json


log = core.getLogger()
firewall_switch_id = None


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.rule1 = False
        self.rule2 = False
        self.rule3 = False
        self.h1 = ""
        self.blocked1 = ""
        self.blocked2 = ""
        self.parse_configuration()

    def parse_configuration(self):
        with open("rules.json", "r") as f:
            self.rule1, self.rule2, self.rule3, self.h1, self.blocked1, self.blocked2 = list(json.load(f).values())

    def _handle_PacketIn(self, event):
        packet = event.parsed

        # Ignore Ip packet
        if packet.type != ethernet.IP_TYPE:
            return

        # Check rules
        if self.rule_applies(packet):
            msg = of.ofp_flow_mod()
            match = of.ofp_match.from_packet(packet)
            msg.match = match
            event.connection.send(msg)

    def rule_applies(self, packet):
        if self.first_rule_applies() and self.packet_dstport_is_80(packet):
            return True
        if self.second_rule_applies() and self.packet_verifies_second_rule(packet):
            return True
        if self.third_rule_applies() and self.packet_between_uncommunicated_hosts(packet):
            return True
        return False

    def first_rule_applies(self):
        return self.rule1

    def second_rule_applies(self):
        return self.rule2

    def third_rule_applies(self):
        return self.rule3

    def packet_dstport_is_80(self, link_packet):
        ip_packet = link_packet.payload

        if ip_packet.protocol not in (ipv4.TCP_PROTOCOL or ipv4.UDP_PROTOCOL):
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == 80:
            log.info("Rule 1: Blocking a flow from " + str(ip_packet.srcip) + " to " + str(ip_packet.dstip))
            return True

        return False

    def packet_verifies_second_rule(self, link_packet):
        # src is host 1, dst port is 5001 and protocol is UDP
        ip_packet = link_packet.payload

        if ip_packet.protocol not in (ipv4.TCP_PROTOCOL or ipv4.UDP_PROTOCOL):
            return False

        if ip_packet.srcip != self.h1:
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == 5001 and ip_packet.protocol == ipv4.UDP_PROTOCOL:
            log.info("Rule 2: Blocking a flow from " + str(ip_packet.srcip) + " to " + str(ip_packet.dstip))
            return True

        return False

    def packet_between_uncommunicated_hosts(self, link_packet):
        ip_packet = link_packet.payload
        if (ip_packet.srcip == self.blocked1 and ip_packet.dstip == self.blocked2) or \
                (ip_packet.srcip == self.blocked2 and ip_packet.dstip == self.blocked1):
            log.info("Rule 3: Blocking a flow from " + str(ip_packet.srcip) + " to " + str(ip_packet.dstip))
            return True
        return False
