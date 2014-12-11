
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        print "Server Init"
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)
        print "Connection Made"

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print "Connection Lost"

    def lineReceived(self, line):
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

        print line

        if(line == 'quit'):
            self.transport.loseConnection()

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)


def main():

    PORT = 10501
    endpoints.serverFromString(reactor, "tcp:" + str(PORT)).listen(PubFactory())
    reactor.run()

if __name__ == "__main__":
    main()