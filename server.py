
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol


class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

        if(line == 'quit'):
            self.transport.loseConnection()

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)


def main():

    PORT = 10501

    """This runs the protocol on port 10501"""
    factory = protocol.PubFactory()
    factory.protocol = Echo
    reactor.listenTCP(PORT,factory)
    reactor.run()

if __name__ == '__main__':
    main()