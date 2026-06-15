from datetime import date

from transaction import Transaction

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


class CommandHandler:
    def __init__(self, store,analyzer,budget_manager):
        self.store = store
        self.analyzer = analyzer
        self.budget_manager = budget_manager

    def handle(self, command):
        parts = command.split()

        if not parts:
            return

        if parts[0] == "add":
            self.handle_add(parts)

        elif parts[0] == "list":
            self.handle_list(parts)
        elif parts[0] == "budget":
            self.handle_budget(parts)

        elif parts[0] == "summary":
            self.handle_summary()

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

    def handle_budget(self, parts):

        if len(parts) != 3:
            print("Usage: budget <category> <limit>")

            return

        category = parts[1]

        try:

            limit = float(parts[2])

        except ValueError:

            print("Budget must be numeric")

            return

        self.budget_manager.set_budget(category, limit)

        print(f"Budget set: {category} -> {limit:.2f} NIS")

    def handle_summary(self):
        summary = self.analyzer.summary()

        print()
        print("===== SUMMARY =====")
        print(f"Income   : {summary['income']:.2f} NIS")
        print(f"Expenses : {summary['expenses']:.2f} NIS")
        print(f"Balance  : {summary['balance']:.2f} NIS")
        print()

        for category, spent in summary["expenses_by_category"].items():

            limit = self.budget_manager.get_budget(category)

            if limit is None:
                print(f"{category}: {spent:.2f} NIS")
                continue

            remaining = limit - spent

            if remaining >= 0:
                color = GREEN
                status = "under budget"
            else:
                color = RED
                status = "over budget"

            print(
                f"{color}"
                f"{category}: {spent:.2f} / {limit:.2f} NIS "
                f"({abs(remaining):.2f} "
                f"{'remaining' if remaining >= 0 else 'over'}) "
                f"[{status}]"
                f"{RESET}"
            )