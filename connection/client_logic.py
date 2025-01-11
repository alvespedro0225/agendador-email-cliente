import socket
from contextlib import contextmanager


class ClientConnector:

    delimiter = "ṕ"
    formating = "UTF-8"

    @classmethod
    @contextmanager
    def socket_connect(cls, server_address):
        mysocket = socket.create_connection(server_address)
        try:
            yield mysocket
        finally:
            mysocket.close()
            print("Closed")

    @classmethod
    def send_message(cls, message, server_address):
        try:
            with cls.socket_connect(server_address) as SOCKET:
                for value in message:
                    SOCKET.send(bytes((value + cls.delimiter), cls.formating))
            return True
        except ConnectionRefusedError:
            return False
