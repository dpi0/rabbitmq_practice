import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Analytics - Received A New Message! --> {body}")
    # ch.basic_ack(delivery_tag=method.delivery_tag)
    # print("---------xxxxxxxxxxxx--------- DONE! Message was processed.")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_direct_exch", exchange_type=ExchangeType.direct
)

queue = channel.queue_declare(queue="analytics_queue", exclusive=True)


channel.queue_bind(
    exchange="my_direct_exch",
    queue="analytics_queue",
    routing_key="analytics_route",
)

channel.basic_consume(
    queue="analytics_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Analytics - Starting Consuming...")
channel.start_consuming()
