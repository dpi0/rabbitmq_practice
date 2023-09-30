import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Consumer2 - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_fanout_exch", exchange_type=ExchangeType.fanout
)

queue = channel.queue_declare(queue="consumer2_queue", exclusive=True)


channel.queue_bind(
    exchange="my_fanout_exch",
    queue="consumer2_queue",
    routing_key="",
    # NOTE: again routing key must be empty for a fanout
)

channel.basic_consume(
    queue="consumer2_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Consumer2 - Starting Consuming...")
channel.start_consuming()
