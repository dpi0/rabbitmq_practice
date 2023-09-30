import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"User - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_topic_exch", exchange_type=ExchangeType.topic
)

queue = channel.queue_declare(queue="user_queue", exclusive=True)


channel.queue_bind(
    exchange="my_topic_exch",
    queue="user_queue",
    routing_key="user.#",
)

channel.basic_consume(
    queue="user_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("User - Starting Consuming...")
channel.start_consuming()
