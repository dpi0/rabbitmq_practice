import pika


def on_msg_recv(ch, method, properties, body):
    print(
        f"Server - Received Request from Client with id --> {properties.correlation_id}"
    )
    MSG_REPLY = f"Hey! Server here, this is my reply to Client with id --> {properties.correlation_id}"
    ch.basic_publish("", routing_key=properties.reply_to, body=MSG_REPLY)


conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.queue_declare(queue="request_queue")

channel.basic_consume(
    queue="request_queue",
    on_message_callback=on_msg_recv,
    auto_ack=True,
)

print("Server - Starting Server...")
channel.start_consuming()
