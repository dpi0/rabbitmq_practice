import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Analytics - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_topic_exch", exchange_type=ExchangeType.topic
)

queue = channel.queue_declare(queue="analytics_queue", exclusive=True)


channel.queue_bind(
    exchange="my_topic_exch",
    queue="analytics_queue",
    routing_key="*.india.*",
)

channel.basic_consume(
    queue="analytics_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Analytics - Starting Consuming...")
channel.start_consuming()
