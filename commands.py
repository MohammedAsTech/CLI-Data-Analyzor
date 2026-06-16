from datetime import date

from transaction import Transaction


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


class CommandHandler:
    def __init__(
        self,
        store,
        analyzer,
        budget_manager,
        chart_generator,
        use_color=True
    ):
        self.store = store
        self.analyzer = analyzer
        self.budget_manager = budget_manager
        self.chart_generator = chart_generator
        self.use_color = use_color

    def handle(self, command):
        try:
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

            elif parts[0] == "chart":
                self.handle_chart(parts)

            elif parts[0] == "delete":
                self.handle_delete(parts)

            elif parts[0] == "export":
                self.handle_export(parts)

            else:
                print("Unknown command")

        except Exception as error:
            print(f"Error: {error}")

    def handle_add(self, parts):
        if len(parts) < 4:
            print("Usage: add <income/expense> <amount> <category> <description> [--date YYYY-MM-DD]")
            return

        tx_type = parts[1]

        try:
            amount = float(parts[2])
        except ValueError:
            print("Error: amount must be a positive number")
            return

        category = parts[3]
        tx_date = date.today().isoformat()

        if "--date" in parts:
            index = parts.index("--date")

            if index + 1 >= len(parts):
                print("Error: --date requires YYYY-MM-DD")
                return

            tx_date = parts[index + 1]
            description = " ".join(parts[4:index])
        else:
            description = " ".join(parts[4:])

        transaction = Transaction(
            tx_type,
            amount,
            category,
            tx_date,
            description
        )

        self.store.add(transaction)

        signed_amount = amount if tx_type == "income" else -amount

        print(
            f"Added: {signed_amount:.2f} NIS | "
            f"{category} | "
            f"{transaction.date}"
        )

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

        if limit <= 0:
            print("Budget must be positive")
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
                amount_text = f"{remaining:.2f} remaining"
            else:
                color = RED
                status = "over budget"
                amount_text = f"{abs(remaining):.2f} over"

            if not self.use_color:
                color = ""
                reset = ""
            else:
                reset = RESET

            print(
                f"{color}"
                f"{category}: {spent:.2f} / {limit:.2f} NIS "
                f"({amount_text}) "
                f"[{status}]"
                f"{reset}"
            )

    def handle_chart(self, parts):
        month = parts[1] if len(parts) > 1 else None
        self.chart_generator.bar_chart(month)

    def handle_delete(self, parts):
        if len(parts) != 2:
            print("Usage: delete <id>")
            return

        try:
            transaction_id = int(parts[1])
        except ValueError:
            print("ID must be a number")
            return

        deleted = self.store.delete(transaction_id)

        if deleted:
            print(f"Deleted transaction #{transaction_id}.")
        else:
            print(f"Transaction #{transaction_id} does not exist.")

    def handle_export(self, parts):
        month = parts[1] if len(parts) > 1 else None

        filename, count = self.store.export(month)

        print(f"Exported {count} transactions to {filename}.")