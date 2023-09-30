import pika
from time import sleep

# from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

# channel.exchange_declare(exchange="", exchange_type=ExchangeType.fanout)
# NOTE: no exchange is declared here

channel.queue_declare(queue="consumer_queue")
# NOTE: we have to declare a queue in case of a default
# and fsr, exclusive=True doesn't work here in default

MSG: str = "Hello!"

while True:
    channel.basic_publish(
        exchange="",
        # NOTE: exchange type must also be empty for a default
        routing_key="consumer_queue",
        body=MSG,
    )

    print(f"Sent message: {MSG}")
    sleep(5)

conn.close()
