import json
import os
class BudgetManager:
    def __init__(self,filepath = "budgets.json"):
        self.filepath = filepath
        self.budgets = {}
        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self.save()
            return

        with open(self.filepath) as file:
            self.budgets = json.load(file)

    def save(self):
        with open(self.filepath, "w") as file:
            json.dump(self.budgets, file, indent=4)

    def set_budget(self, category, limit):
        self.budgets[category.lower()] = float(limit)
        self.save()

    def get_budget(self, category):
        return self.budgets.get(category.lower())


