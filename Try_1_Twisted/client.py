from twisted.internet import reactor, protocol

class SubscribeProtocol(protocol.Protocol):

    """Once connected, send a message, then print the result."""
    def connectionMade(self):
        self.sendMessage("hello, world!")
        reactor.callLater(1, self.sendMessage, "Two")
        reactor.callLater(2, self.sendMessage, "One")
        reactor.callLater(3, self.sendMessage, "quit")
        reactor.callLater(4, self.transport.loseConnection)

    def dataReceived(self, data):
        print "Server Message: {}".format(data)

    def sendMessage(self, msg):
        self.transport.write(msg)

    def subscribeToService(self, serviceName):
        pass

    def unsubscribeFromService(self, serviceName):
        pass

    def publishToService(self, serviceName):
        pass

class SubscribeFactory(protocol.ClientFactory):

##   protocol = SubscribeProtocol

##    def __init__(self):
##        print "Factory started."

    def buildProtocol(self, addr):
        return SubscribeProtocol()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:" + str(reason)
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

#TODO: SubscriptionProducerObject

def main():

    ADDRESS = "localhost"
    PORT = 10501

    factory = SubscribeFactory()

    reactor.connectTCP(ADDRESS, PORT, factory)
    reactor.run()

if __name__ == '__main__':
    main()