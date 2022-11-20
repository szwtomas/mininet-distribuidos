class Rule():
    def __init__(self, is_activated=False):
        self._is_activated = is_activated

    def is_activated(self):
        return self._is_activated

    def set_is_activated(self, activated):
        self._is_activated = activated

    def evaluate(self, link_packet):
        pass
