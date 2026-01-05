from client.network import ClientNetwork

class ConsoleUI:
    def __init__(self, username):
        self.client = ClientNetwork(username)

    def run(self):
        self.client.connect()
        print("Вы подключены. Введите сообщение или /file <путь> для отправки файла.")

        # Приём сообщений
        for msg in self.client.receive():
            print(f"[{msg['sender']}] {msg['text']}")
            if msg.get('file'):
                print(f!Файл доступен: {msg['file']}")

        # Отправка сообщений
        while True:
            text = input("> ")
            if text.startswith('/file '):
                filepath = text[7:]
                self.client.send_message("", file_path=filepath)
            else:
                self.client.send_message(text)
