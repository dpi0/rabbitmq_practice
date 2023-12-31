from driver import ProdClass
from time import sleep
from random import randint


producer = ProdClass()

channel = producer.create_channel()

channel.queue_declare(queue="FirstQueue")

MSG_ID = 1
MSG_CONTENT = "Nice Tie!"

while True:
    msg = f"Message id: '{MSG_ID}' & content = '{MSG_CONTENT}"

    channel.basic_publish(exchange="", routing_key="FirstQueue", body=msg)
    # NOTE: selects the def exchange.
    # NOTE: queue is "FIrstQueue"

    print(f"Message id: '{MSG_ID}' was successfully sent!")

    sleep(randint(1, 3))
    MSG_ID += 1
    # sleep for some time before sending another msg

# producer.connection.close()
