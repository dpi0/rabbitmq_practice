from pika import ConnectionParameters, BlockingConnection


class ProdClass:
    def __init__(self) -> None:
        self.connection_params = ConnectionParameters("localhost")
        self.connection = BlockingConnection(self.connection_params)

    def create_channel(self):
        channel = self.connection.channel()
        return channel
