# from producer import ProdClass

from driver import ProdClass

from time import sleep
from random import randint

producer = ProdClass()

channel = producer.create_channel()

channel.queue_declare(queue="FirstQueue")

channel.basic_qos(prefetch_count=1)
# NOTE: prefetch_count = 1, makes sure that consumer
# only processes 1 msg at a time even though more in queue


def on_msg_recv(ch, method, properties, body):
    # NOTE: we will simulate a fake processes going on
    # i.e the consumer is processing the msg it received
    # so the consumer's ack sent will be realistic
    # as it is after processing it

    processing_time = randint(1, 10)

    print(
        f"Received New Message,  \n content: {body}, it will take {processing_time} seconds to process it"  # noqa: E501
    )

    sleep(processing_time)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    # NOTE: THIS is the manually ack we can do
    # SIDENOTE: delivery_tag is to make sure
    # we ONLY the ACK the msg we processed and recevied

    print("---------xxxxxxxxxxxx--------- DONE! Message was processed.")


channel.basic_consume(
    queue="FirstQueue",
    # auto_ack=True,
    on_message_callback=on_msg_recv,
)
# NOTE: auto_ack = True, when set to TRUE, once consumer pulls the msg off the queue,
# msg is removed from the queue, as it is auto ack
# NOTE: we can manually do this

print("Starting Consuming...")
channel.start_consuming()
