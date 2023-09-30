import pika
from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_topic_exch", exchange_type=ExchangeType.topic
)
# NOTE: change the topic & exchange name here too

MSG_TO_USER: str = "Hello my man!"
MSG_TO_ANALYTICS: str = "Hello Analytics"


channel.basic_publish(
    exchange="my_topic_exch",
    routing_key="user.india.yyyy",
    body=MSG_TO_USER,
)

print(f"Sent message: {MSG_TO_USER}")

conn.close()
