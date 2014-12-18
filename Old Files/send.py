#!/usr/bin/env python
import pika
import time
import threading

class rabbitTest:

    def __init__(self, in_address):
        self._connection = pika.SelectConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = connection.channel()

        self.queueName = ''

        self.consumeThread = threading.Thread(target = self._consume)
        self.consumeThread.daemon = True
        self.consumeThread.start()

    def declareTopic(self, topicName):
        channel.exchange_declare(exchange=topicName, type='fanout')

    def subscribeToTopic(self, topicName, callback):
        #Create a random queue and bind 'logs' to it.
        #Exclusive means remove the queue once the connection is closed.
        result = channel.queue_declare(exclusive=True)
        self.queueName = result.method.queue

        channel.queue_bind(exchange='logs',
                           queue=self.queueName)

        channel.basic_consume(callback, queue = self.queueName, noack=True)

    #This needs to be threaded.
    def _consume(self):
        self.channel.start_consuming()

    def sendMessage(self, msg):
        channel.basic_publish(exchange='logs',
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
    sendMessage('Hello World')
    time.sleep(1)
