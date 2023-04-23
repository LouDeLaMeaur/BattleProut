from config import *
import socket

class TCPClient:
    def __init__(self):
        self.ip = IP
        self.port = PORT
        self.socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        self.socket.connect((self.ip, self.port))

    def send(self):
        pass

    def recv(self):
        pass

    def disconnect(self):
        self.socket.close()