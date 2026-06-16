import sys

from analyzer import Analyzer
from budget import BudgetManager
from chart import ChartGenerator
from commands import CommandHandler
from store import TransactionStore


def main():
    use_color = "--no-color" not in sys.argv

    store = TransactionStore()
    analyzer = Analyzer(store)
    budget_manager = BudgetManager()
    chart_generator = ChartGenerator(analyzer)

    handler = CommandHandler(
        store,
        analyzer,
        budget_manager,
        chart_generator,
        use_color
    )

    try:
        while True:
            command = input("> ").strip()

            if command == "exit":
                break

            handler.handle(command)

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()