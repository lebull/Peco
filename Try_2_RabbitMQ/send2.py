#!/usr/bin/env python
import pika
import time
import threading

class rabbitTest:

    def __init__(self, in_address):
        self._connection = pika.SelectConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self._connection.channel(self.onChannelOpen)

        self.queueName = ''

    def onChannelOpen(self):
        pass

    def startConsumer(self):
        # Step #1: Connect to RabbitMQ
        try:
            # Loop so we can communicate with RabbitMQ
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            # Gracefully close the connection
            self._connection.close()
            # Loop until we're fully closed, will stop on its own
            self._connection.ioloop.start()



    def declareTopic(self, topicName):
        self.channel.exchange_declare(self.on_exchange_declareok, exchange=topicName, type='fanout')

    ###-------------------------------------------------------------------
    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        LOGGER.info('Exchange declared')
        self.setup_queue(self.QUEUE)

    def subscribeToTopic(self, topicName, callback):
        #Create a random queue and bind 'logs' to it.
        #Exclusive means remove the queue once the connection is closed.
        result = channel.queue_declare(exclusive=True)
        self.queueName = result.method.queue

        channel.queue_bind(exchange=topicName,
                           queue=self.queueName)

        channel.basic_consume(callback, queue = self.queueName, noack=True)

    def sendMessage(self, topicName, msg):
        channel.basic_publish(exchange=topicName,
                          routing_key='',
                          body=msg)
        print "Outbound: {}".format(msg)

    #Todo:  What happens if the connection is closed while the consume thread is still consuming?
    def end(self):
        self._connection.close()


#Callback for receiving messages. ch, method, properties, body
def receiveMessage(ch, method, properties, body):
    print "Inbound: {}".format(body)


testCase = rabbitTest('localhost')
testCase.declareTopic('logs')
testCase.subscribeToTopic('logs', recieveMessage)

for i in range(60):
    sendMessage('Hello World', 'logs')
    time.sleep(1)
