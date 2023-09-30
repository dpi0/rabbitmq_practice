import pika
from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_fanout_exch", exchange_type=ExchangeType.fanout
)

MSG: str = "Hello ALL Consumers!"


channel.basic_publish(
    exchange="my_fanout_exch",
    routing_key="",
    # NOTE: routing key must be empty for a fanout
    body=MSG,
)

print(f"Sent message: {MSG}")

conn.close()
