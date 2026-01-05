from ui import ConsoleUI
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Используйте: python main.py <имя_пользователя>")
        sys.exit(1)

    username = sys.argv
