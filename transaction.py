class Transaction:
    def __init__(self,id,type,amount,category,date,description ):
        if type is not "income" or type is not "expense":
            raise ValueError("Type must be 'income' or 'expense'")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.id = id
        self.type = type
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
    def to_dict(self):
        return {"id" : self.id,"type" : self.type,"amount": self.amount,"category": self.category,"date": self.date,"description": self.description}
    def __str__(self):
        return str(self.to_dict())
