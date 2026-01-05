import socket
import json
from shared.protocol import create_message, parse_message
import config

class ClientNetwork:
    def __init__(self, username):
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((config.SERVER_HOST, config.SERVER_PORT))
        self.sock.send(self.username.encode('utf-8'))

    def send_message(self, text, file_path=None):
        msg = create_message(self.username, text, file_path)
        self.sock.send(msg)

    def receive(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if data:
                    msg = parse_message(data)
                    if msg:
                        yield msg
            except:
                break
