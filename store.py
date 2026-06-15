import csv

from transaction import Transaction


class TransactionStore:
    def __init__(self,filepath = "transactions.csv"):
        self.transactions = []
        self.filepath = filepath

    def load(self):
        with open(self.filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")

            for row in reader:
                transaction = Transaction(
                    int(row["id"]),
                    row["type"],
                    float(row["amount"]),
                    row["category"],
                    row["date"],
                    row["description"]
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


