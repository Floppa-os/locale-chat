import socket
import threading
import os
from shared.protocol import parse_message, create_file_chunk
from shared.utils import get_file_hash, split_file
import config

class MessengerServer:
    def __init__(self):
        self.clients = {}  # {addr: username}
        self.messages = []  # Хранилище сообщений
        self.files = {}     # {file_id: {'chunks': [], 'total': N}}

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((config.SERVER_HOST, config.SERVER_PORT))
        sock.listen(5)
        print(f"[SERVER] Запущен на {config.SERVER_HOST}:{config.SERVER_PORT}")

        while True:
            client_sock, addr = sock.accept()
            print(f"[SERVER] Подключение от {addr}")
            threading.Thread(target=self.handle_client, args=(client_sock, addr)).start()

    def handle_client(self, client_sock, addr):
        try:
            # Первое сообщение — имя пользователя
            username = client_sock.recv(1024).decode('utf-8').strip()
            self.clients[addr] = username
            print(f"[SERVER] Пользователь {username} подключился")

            while True:
                data = client_sock.recv(4096)
                if not data:
                    break

                msg = parse_message(data)
                if msg:
                    if msg['type'] == 'message':
                        self.broadcast(msg, client_sock)
                    elif msg['type'] == 'file_request':
                        self.send_file(msg['file_id'], client_sock)

        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            client_sock.close()
            if addr in self.clients:
                del self.clients[addr]

    def broadcast(self, msg, sender_sock):
        """Отправить сообщение всем клиентам"""
        for addr, sock in self.clients.items():
            if sock != sender_sock:
                try:
                    sock.sendall(json.dumps(msg).encode('utf-8'))
                except:
                    pass

    def send_file(self, file_id, client_sock):
        """Отправить файл клиенту по ID"""
        if file_id not in self.files:
            return

        file_data = self.files[file_id]
        for i, chunk in enumerate(file_data['chunks']):
            packet = create_file_chunk(chunk, i, file_data['total_chunks'])
            client_sock.send(json.dumps(packet).encode('utf-8'))
