from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
import json
from .constants import DROP_PORT, HTTP_PORT, RULES_PATH


log = core.getLogger()
firewall_switch_id = None


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.rule1 = False
        self.rule2 = False
        self.rule3 = False
        self.h1 = ""
        self.ip_blocked1 = ""
        self.ip_blocked2 = ""
        self.parse_configuration()


    def parse_configuration(self):
        with open("rules.json", "r") as f:
            rules = json.load(f)
            self.rule1 = rules["r1_enabled"]
            self.rule2 = rules["r2_enabled"]
            self.rule3 = rules["r3_enabled"]
            self.h1 = rules["r2_blocked_host"]
            self.blocked1 = rules["r3_first_blocked"]
            self.blocked2 = rules["r3_second_blocked"]

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
        if self.rule_1 and self.packet_dstport_is_80(packet):
            return True
        if self.rule_2 and self.packet_verifies_second_rule(packet):
            return True
        if self.rule_3 and self.packet_between_uncommunicated_hosts(packet):
            return True

        return False


    def packet_dstport_is_80(self, link_packet):
        ip_packet = link_packet.payload

        if not self._is_udp_or_tcp(ip_packet.protocol):
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == HTTP_PORT:
            self._log_rule_block(1, ip_packet.srcip, ip_packet.dstip)
            return True

        return False


    def packet_verifies_second_rule(self, link_packet):
        # src is host 1, dst port is 5001 and protocol is UDP
        ip_packet = link_packet.payload

        if not self._is_udp_or_tcp(ip_packet.protocol):
            return False

        if ip_packet.srcip != self.h1:
            return False

        transport_packet = ip_packet.payload
        if transport_packet.dstport == DROP_PORT and ip_packet.protocol == ipv4.UDP_PROTOCOL:
            self._log_rule_block(2, ip_packet.srcip, ip_packet.dstip)
            return True

        return False


    def packet_between_uncommunicated_hosts(self, link_packet):
        ip_packet = link_packet.payload
        if self._should_block_packet(ip_packet):    
            self._log_rule_block(3, ip_packet.srcip, ip_packet.dstip)
            return True
        return False


    def _should_block_packet(self, ip_packet):
        is_blocked_2 = ip_packet.srcip == self.ip_blocked2 and ip_packet.dstip == self.ip_blocked1
        is_blocked_1 = ip_packet.srcip == self.ip_blocked1 and ip_packet.dstip == self.ip_blocked2 
        return is_blocked_1 or is_blocked_2


    def _log_rule_block(rule_number, srcip, dstip):
        log_message = "Rule " + str(rule_number) + ": Blocking a flow from " + str(srcip) + " to " + str(dstip) 
        log.info(log_message)


    def _is_udp_or_tcp(protocol):
        return protocol in (ipv4.TCP_PROTOCOL or ipv4.UDP_PROTOCOL)
