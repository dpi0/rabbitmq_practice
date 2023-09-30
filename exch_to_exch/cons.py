import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Consumer - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_second_fanout_exch", exchange_type=ExchangeType.fanout
)

channel.queue_declare(queue="fanout_consumer_queue")

channel.queue_bind(
    exchange="my_second_fanout_exch",
    queue="fanout_consumer_queue",
    routing_key="",
    # NOTE: fanout exchange no routing key
)

channel.basic_consume(
    queue="fanout_consumer_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Consumer - Starting Consuming from my_second_fanout_exch...")
channel.start_consuming()
