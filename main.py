from commands import CommandHandler
from store import TransactionStore


def main():
    store = TransactionStore()
    handler = CommandHandler(store)

    while True:
        command = input("> ").strip()

        if command == "exit":
            break

        handler.handle(command)


if __name__ == "__main__":
    main()