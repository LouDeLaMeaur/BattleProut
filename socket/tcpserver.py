import socket

class TCPServer:
    def __init__(self):
        self.port = 8000
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_donnee = None

    def listening(self):
        self.socket_ecoute.bind(("", self.port))
        self.socket_ecoute.listen(1)
        print('listening on port ', self.port)
        self.socket_donnee, ADDR = self.socket_ecoute.accept()
        self.socket_ecoute.close()

    def send(self, msg):
        payload = msg.encode('utf-8')
        self.socket_donnee.send(payload)

    def receive(self):
        payload = self.socket_donnee.recv(256)
        return payload.decode('utf-8')

    def close(self):
        self.socket_donnee.close()

if __name__ == "__main__":
    server = TCPServer()
    server.listening()
    server