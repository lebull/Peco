from PublisherConnection import Publisher
from SubscriberConnection import SubscriberConnection

import time
import random

#TODO: There are weird errors being thrown on stop and it's not stopping smoothly.  Not quite sure what's happening.
#TODO: Looks like there's a hanging thread.
#TODO: The queue name is pointless in this case, I'm pretty sure.  Trash it.

url = 'amqp://guest:guest@localhost:5672/%2F?'
#Params
url += '&'.join(['connection_attempts=3', 'heartbeat_interval=3600'])

#========================================================================================
#   Test Subscriber
#========================================================================================

subscriberConnection = SubscriberConnection(
    url = url, 
    exchange = 'demo', 
    binding_key = 'demo.1'
)


#========================================================================================
#   Test Publisher
#========================================================================================
publisherConnection = Publisher(
    amqp_url = url,
    exchange = 'demo',
    queue = 'trash',
    routing_key = 'demo.2'
)

try:
    for i in range(30):
        time.sleep(1)
        publisherConnection.publisherConnection.publish_message(str(random.randint(0, 10)))

    publisherConnection.stop()
    subscriberConnection.stop()

except KeyboardInterrupt:
    publisherConnection.stop()
    subscriberConnection.stop()