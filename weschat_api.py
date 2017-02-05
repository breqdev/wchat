import socket
from select import select

class WesChat:
    def __init__(self, host, handshake, port=8888, name=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.post(handshake)
        if name != None:
            self.post("/uname "+name)
    def post(self, message):
        self.s.send(message.encode())
    def get_messages(self):
        if select([self.s], [], [], 0)[0] == [self.s]:
            return self.s.recv(4096).decode()
    def wait_for_message(self):
        select([self.s], [], [])
        return self.s.recv(4096).decode()

