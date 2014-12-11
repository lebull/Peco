
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import reactor, protocol


# a client protocol

class SubscribeProtocol(protocol.Protocol):

    """Once connected, send a message, then print the result."""
    def connectionMade(self):
        self.transport.write("hello, world!")
        reactor.callLater(1, self.sendMessage, "Two")
        reactor.callLater(2, self.sendMessage, "One")
        reactor.callLater(3, self.sendMessage, "quit")


    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server: {}".format(data)
    
    def connectionLost(self, reason):
        print "connection lost"

    def sendMessage(self, message):
        print "Client: {}".format(message)
        self.transport.write(message)

    def subscribe(self, callback):
        pass

    def registerService(self):
        pass

    def publish(self):
        pass

class EchoFactory(protocol.ClientFactory):
    protocol = SubscribeProtocol

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:" + str(reason)
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


def main():

    ADDRESS = "127.0.0.1"
    PORT = 10501

    f = EchoFactory()

    reactor.connectTCP(ADDRESS, PORT, f)
    reactor.run()

if __name__ == '__main__':
    main()