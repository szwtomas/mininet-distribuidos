from mininet.topo import Topo

class LinearTopology(Topo):

    def __init__(self, n):
        Topo.__init__(self)

        switchCount = int(n)

        if switchCount <= 0:
            raise ValueError("switchCount must be greater than 0")

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        switches = []
        for i in range(switchCount):
            switchName = "s" + str(i+1)
            newSwitch = self.addSwitch(switchName)
            switches.append(newSwitch)

        self.addLink(h1, switches[0])
        self.addLink(h2, switches[0])

        self.addLink(h3, switches[len(switches)-1])
        self.addLink(h4, switches[len(switches)-1])

        for i in range(1, len(switches)-1):
            self.addLink(switches[i-1], switches[i])


topos = { "linearTopo": lambda x: LinearTopology(x) }
