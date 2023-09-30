import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Payments - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_topic_exch", exchange_type=ExchangeType.topic
)
# NOTE: change the exchange & exchange_type for TOPICS

queue = channel.queue_declare(queue="payments_queue", exclusive=True)


channel.queue_bind(
    exchange="my_topic_exch",
    queue="payments_queue",
    routing_key="#.payments",
)
# NOTE: here too change exchange
# IMP: hash.payments can mean, XXXX.payments, XXXX.YYYY.payments ...

channel.basic_consume(
    queue="payments_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Payments - Starting Consuming...")
channel.start_consuming()
