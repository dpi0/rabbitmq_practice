import pika

# from pika.exchange_type import ExchangeType


def on_msg_recv(ch, method, properties, body):
    print(f"Consumer - Received A New Message! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

# channel.exchange_declare(
#     exchange="my_topic_exch", exchange_type=ExchangeType.topic
# )
# NOTE: no exchange is declared for default

channel.queue_declare(queue="consumer_queue")
# fsr, exclusive=True doesn't work here in default


# channel.queue_bind(
#     exchange="my_topic_exch",
#     queue="user_queue",
#     routing_key="user.#",
# )
# NOTE: also no binding is done for default

channel.basic_consume(
    queue="consumer_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Consumer - Starting Consuming...")
channel.start_consuming()
