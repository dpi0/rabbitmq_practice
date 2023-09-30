import pika
from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="my_first_direct_exch", exchange_type=ExchangeType.direct
)
channel.exchange_declare(
    exchange="my_second_fanout_exch", exchange_type=ExchangeType.fanout
)
# NOTE: declare two exchanges one is DIRECT other is FANOUT


channel.exchange_bind("my_second_fanout_exch", "my_first_direct_exch")
# NOTE: bind those two exchanges my_second <-- my_first this is the order

channel.queue_declare(queue="consumer_queue")

MSG: str = "Hello! I've been through many exchanges"

channel.basic_publish(
    exchange="my_first_direct_exch",
    # IMP: this message is first sent to DIRECT
    # then it auto goes to FANOUT
    routing_key="",
    # IMP: as it is DIRECt, it doesn't need a routing key
    body=MSG,
)

print(f"Sent message to my_first_direct_exch: {MSG}")

conn.close()
