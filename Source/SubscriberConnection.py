#!/usr/bin/env python
import pika
import sys

import threading
import time


#TODO: This is synchronos.  Should we find an asynchronos version cause of performance?
class SubscriberConnection(threading.Thread):

  def __init__(self, url, exchange, binding_key):
    threading.Thread.__init__(self)

    #TODO: BRING ON THE PARAMETERS.  PUT EM RIGHT IN THE KISSER



    self._connection = pika.BlockingConnection(pika.URLParameters(url))
    self.channel = self._connection.channel()

    self.channel.exchange_declare(exchange=exchange,
                             type='topic')

    result = self.channel.queue_declare(exclusive=True)
    self._queue_name = result.method.queue


    print "Binding Key: {}".format(binding_key)
    self.channel.queue_bind(exchange=exchange,
                       queue=self._queue_name,
                       routing_key=binding_key)

    self.channel.basic_consume(self.onMessageReceive,
                          queue=self._queue_name,
                          no_ack=True)

    self.running = False

    self.start()

  def onMessageReceive(self, ch, method, properties, body):
    print " [x] {}:{}".format(method.routing_key, body)

  def run(self):
    self.running = True
    self.channel.start_consuming()

  def stop(self):
    self.channel.stop_consuming()
    self.running = False


def main():

  #url='localhost'

  url = 'amqp://guest:guest@localhost:5672/%2F?'
  #Params
  url += '&'.join(['connection_attempts=3', 'heartbeat_interval=3600'])

  exchange = 'message'
  binding_key = "example.text"


  subscriberConnection = SubscriberConnection(url, exchange, binding_key)


  try:
    while(1):
        time.sleep(0.5)

  except KeyboardInterrupt:
      subscriberConnection.stop()

if __name__ == '__main__':
  main()