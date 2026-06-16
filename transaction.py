from datetime import datetime


class Transaction:
    def __init__(self, type, amount, category, date, description, id=None):
        if type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if not category:
            raise ValueError("Category cannot be empty")

        datetime.strptime(date, "%Y-%m-%d")

        self.id = id
        self.type = type
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["type"],
            float(data["amount"]),
            data["category"],
            data["date"],
            data["description"],
            int(data["id"])
        )

    def __str__(self):
        return str(self.to_dict())