from pox.core import core
from firewall.firewall import Firewall

log = core.getLogger()


class Controller:
    def __init__(self, firewall_switch):
        self.firewall_switch = firewall_switch

    def start(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        if self.firewall_switch == event.dpid:
            print("firewall")
            log.info("Firewall set")
            self.firewall = Firewall()


def launch(firewall_switch):
    controller = Controller(firewall_switch)
    controller.start()
