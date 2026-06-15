from datetime import date

import matplotlib.pyplot as plt


class ChartGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def bar_chart(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")

        data = self.analyzer.by_category(month)

        if not data:
            print("No expense data for this month")
            return

        categories = [category for category, total in data]
        amounts = [total for category, total in data]

        plt.figure(figsize=(10, 6))

        bars = plt.barh(categories, amounts)

        for bar, amount in zip(bars, amounts):
            plt.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f"{amount:.2f}",
                va="center"
            )

        plt.title(f"Spending by Category ({month})")
        plt.xlabel("Amount (NIS)")
        plt.ylabel("Category")

        plt.tight_layout()

        filename = f"spending_{month}.png"
        self.save_png(filename)

    def save_png(self, path):
        plt.savefig(path)
        plt.close()

        print(f"Chart saved to {path}")