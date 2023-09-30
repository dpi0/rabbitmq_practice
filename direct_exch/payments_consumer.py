import pika
from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Payments - Received A New Message! --> {body}")
    # ch.basic_ack(delivery_tag=method.delivery_tag)
    # print("---------xxxxxxxxxxxx--------- DONE! Message was processed.")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_direct_exch", exchange_type=ExchangeType.direct
)

queue = channel.queue_declare(queue="payments_queue", exclusive=True)
# exclusive means queue will be deleted once conn closes


channel.queue_bind(
    exchange="my_direct_exch",
    queue="payments_queue",
    routing_key="payments_route",
)

channel.basic_consume(
    queue="payments_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Payments - Starting Consuming...")
channel.start_consuming()
