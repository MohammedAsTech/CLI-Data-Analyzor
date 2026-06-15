from datetime import date

from transaction import Transaction


class CommandHandler:
    def __init__(self, store):
        self.store = store

    def handle(self, command):
        parts = command.split()

        if not parts:
            return

        if parts[0] == "add":
            self.handle_add(parts)

        elif parts[0] == "list":
            self.handle_list(parts)

        else:
            print("Unknown command")

    def handle_add(self, parts):
        if len(parts) < 4:
            print("Usage: add <income/expense> <amount> <category> <description>")
            return

        tx_type = parts[1]

        try:
            amount = float(parts[2])
        except ValueError:
            print("Amount must be a number")
            return

        category = parts[3]
        description = " ".join(parts[4:])

        try:
            transaction = Transaction(
                tx_type,
                amount,
                category,
                date.today().isoformat(),
                description
            )

            self.store.add(transaction)

            signed_amount = amount if tx_type == "income" else -amount

            print(
                f"Added: {signed_amount:.2f} NIS | "
                f"{category} | "
                f"{transaction.date}"
            )

        except ValueError as error:
            print(error)

    def handle_list(self, parts):
        category = parts[1] if len(parts) > 1 else None

        transactions = self.store.list_transactions(category)

        for transaction in transactions:
            signed_amount = (
                transaction.amount
                if transaction.type == "income"
                else -transaction.amount
            )

            print(
                f"{transaction.id} | "
                f"{transaction.date} | "
                f"{transaction.type} | "
                f"{transaction.category} | "
                f"{signed_amount:.2f} | "
                f"{transaction.description}"
            )