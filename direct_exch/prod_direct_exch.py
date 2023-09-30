import pika
from pika.exchange_type import ExchangeType

# from time import sleep
# from random import randint, choice

conn_params = pika.ConnectionParameters("localhost")
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(
    exchange="analytics_exch", exchange_type=ExchangeType.direct
)

MSG: str = "Hello Analytics"
# MSG_ID: int = 1

channel.basic_publish(
    exchange="my_direct_exch", routing_key="analytics_route", body=MSG
)

print(f"Sent message: {MSG}")

# routes: list[str] = ["analytics_route", "payments_route"]

# while MSG_ID < 10:
#     msg = f"Message id: '{MSG_ID}' & content = '{MSG}"

#     channel.basic_publish(
#         exchange="my_direct_exch", routing_key=choice(routes), body=MSG
#     )

#     print(f"Message id: '{MSG_ID}' was successfully sent!")

#     sleep(randint(1, 3))
#     MSG_ID += 1

conn.close()
