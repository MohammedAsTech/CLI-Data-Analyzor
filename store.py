import csv

from transaction import Transaction


class TransactionStore:
    def __init__(self,filepath = "transactions.csv"):
        self.transactions = []
        self.filepath = filepath
    def load(self):
        with open(self.filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transaction = Transaction(int(row["id"]),row["type"],float(row["amount"]),row["category"],row["date"],row["description"])
                self.transactions.append(transaction)
    