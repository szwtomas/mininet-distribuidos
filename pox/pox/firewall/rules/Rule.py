class Rule():

    def __init__(self, is_activated=False):
        self.is_activated = is_activated

    def is_activated(self):
        return self.is_activated

    def set_is_activated(self, activated):
        self.is_activated = activated

    def verify(self, link_packet):
        pass
