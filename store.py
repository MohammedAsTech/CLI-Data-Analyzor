import csv
import os

from transaction import Transaction


class TransactionStore:
    def __init__(self, filepath="transactions.csv"):
        self.transactions = []
        self.filepath = filepath
        self.load()

    def load(self):
        self.transactions.clear()

        if not os.path.exists(self.filepath):
            self.save()
            return

        with open(self.filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")

            for row in reader:
                transaction = Transaction(

                    row["type"],
                    float(row["amount"]),
                    row["category"],
                    row["date"],
                    row["description"],
                    int(row["id"])
                )
                self.transactions.append(transaction)

    def save(self):
        with open(self.filepath, "w", newline="") as csvfile:
            fieldnames = [
                "id",
                "type",
                "amount",
                "category",
                "date",
                "description"
            ]

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                delimiter="|"
            )

            writer.writeheader()

            for transaction in self.transactions:
                writer.writerow(transaction.to_dict())

    def add(self, transaction):
        if transaction.id is None:
            transaction.id = self.next_id()

        self.transactions.append(transaction)
        self.save()

    def delete(self, id):
        for transaction in self.transactions:
            if transaction.id == id:
                self.transactions.remove(transaction)
                self.save()
                return True

        return False

    def next_id(self):
        if not self.transactions:
            return 1

        return max(transaction.id for transaction in self.transactions) + 1

    def export(self, month=None):
        if month is None:
            transactions = self.transactions
            filename = "export_all.csv"
        else:
            transactions = [
                transaction for transaction in self.transactions
                if transaction.date.startswith(month)
            ]
            filename = f"export_{month}.csv"

        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "id",
                "type",
                "amount",
                "category",
                "date",
                "description"
            ]

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                delimiter="|"
            )

            writer.writeheader()

            for transaction in transactions:
                writer.writerow(transaction.to_dict())

        return filename, len(transactions)