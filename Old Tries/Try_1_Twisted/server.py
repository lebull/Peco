from twisted.application import internet, service
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

from sys import stdout

class PubProtocol(protocol.Protocol):
    def __init__(self, factory):
        print "Protocal Init"
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)
        self.transport.write("Welcome!")
        print "Connection Made"

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print "Connection Lost"

    def dataReceived(self, data):
        print "{}: {}".format(self.transport.getPeer(), data)
        self.transport.write("Server: {}".format(data))


##    def lineReceived(self, line):
##
##        print line
##        self.sendLine("Line: {}".format(line))

##        for c in self.factory.clients:
##            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

##        if(line == 'quit'):
##            self.transport.loseConnection()

class PubFactory(protocol.Factory):


    def __init__(self):
        print "Factory Init."
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)

class ServiceContainer:

    #Dictionary of registered service names.  The key is the service name, the value is the set of clients.
    services = {}

    def __init__(self):
        pass

    def registerService(self, name):
        #test if service exists.
        #if not, register.

        services[name] = set()


    #Subscribe and publish
    def subscribeClientToService(self, client, serviceName):
        services[serviceName].add(client)

    def unsubscribeClientFromService(self, client, serviceName):
        pass

    def publishToService(self, serviceName, data):
        pass

    def addPublishCallback(self, inFunction):
        #Hooks up a callback to be called when ANY service is published to.
        #parameters will be data, client list
        pass
def main():

    PORT = 10501
    reactor.listenTCP(PORT, PubFactory())
    reactor.run()

if __name__ == "__main__":
    main()