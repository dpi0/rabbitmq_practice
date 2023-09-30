import pika
import uuid


def on_msg_recv(ch, method, properties, body):
    print(f"Client - Received Reply From Server! --> {body}")


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

reply_queue = channel.queue_declare(queue="", exclusive=True)

channel.basic_consume(
    queue=reply_queue.method.queue,
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

channel.queue_declare(queue="request_queue")


MSG: str = "Hey! Client here, Server can you reply?"

CORRELATION_ID: str = str(uuid.uuid4())

print(f"Client - Sending Request to Server with id --> {CORRELATION_ID}")

channel.basic_publish(
    exchange="",
    routing_key="request_queue",
    body=MSG,
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue, correlation_id=CORRELATION_ID
    ),
)

print("Client - Starting Client...")
channel.start_consuming()
