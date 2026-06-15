from datetime import date


class Analyzer:
    def __init__(self, store):
        self.store = store

    def summary(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")

        total_income = 0
        total_expenses = 0
        expenses_by_category = {}

        for transaction in self.store.transactions:
            if not transaction.date.startswith(month):
                continue

            if transaction.type == "income":
                total_income += transaction.amount

            elif transaction.type == "expense":
                total_expenses += transaction.amount

                if transaction.category not in expenses_by_category:
                    expenses_by_category[transaction.category] = 0

                expenses_by_category[transaction.category] += transaction.amount

        return {
            "income": total_income,
            "expenses": total_expenses,
            "balance": total_income - total_expenses,
            "expenses_by_category": expenses_by_category
        }

    def by_category(self, month=None):
        summary = self.summary(month)

        return sorted(
            summary["expenses_by_category"].items(),
            key=lambda item: item[1],
            reverse=True
        )

    def monthly_totals(self):
        months = {}

        for transaction in self.store.transactions:
            month = transaction.date[:7]

            if month not in months:
                months[month] = {
                    "income": 0,
                    "expense": 0
                }

            if transaction.type == "income":
                months[month]["income"] += transaction.amount

            elif transaction.type == "expense":
                months[month]["expense"] += transaction.amount

        result = []

        for month in sorted(months.keys()):
            result.append(
                (
                    month,
                    months[month]["income"],
                    months[month]["expense"]
                )
            )

        return result