"""
Tests for analyzer.py
Covers: summary calculations, category normalization, by_category ordering,
        monthly_totals, edge cases, floating-point accuracy, invariants.
"""
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import Analyzer
from helpers import TempDirTest, make_analyzer, make_store, make_transaction


class TestAnalyzerSummaryBasic(TempDirTest, unittest.TestCase):

    def _summary(self, month="2024-01"):
        return make_analyzer(self.store).summary(month=month)

    def setUp(self):
        super().setUp()
        self.store = make_store(self.tmp)

    def test_empty_store_all_zeros(self):
        s = self._summary()
        self.assertEqual(s["income"], 0)
        self.assertEqual(s["expenses"], 0)
        self.assertEqual(s["balance"], 0)
        self.assertEqual(s["expenses_by_category"], {})

    def test_income_only(self):
        self.store.add(make_transaction(type="income", amount=1000, date="2024-01-10"))
        s = self._summary()
        self.assertEqual(s["income"], 1000)
        self.assertEqual(s["expenses"], 0)
        self.assertEqual(s["balance"], 1000)

    def test_expense_only(self):
        self.store.add(make_transaction(type="expense", amount=200, date="2024-01-05", category="food"))
        s = self._summary()
        self.assertEqual(s["income"], 0)
        self.assertEqual(s["expenses"], 200)
        self.assertEqual(s["balance"], -200)

    def test_balance_income_minus_expenses(self):
        self.store.add(make_transaction(type="income", amount=3000, date="2024-01-01"))
        self.store.add(make_transaction(type="expense", amount=700, date="2024-01-10", category="food"))
        s = self._summary()
        self.assertEqual(s["balance"], 2300)

    def test_balance_can_be_negative(self):
        self.store.add(make_transaction(type="expense", amount=500, date="2024-01-01", category="x"))
        self.assertEqual(self._summary()["balance"], -500)

    def test_balance_can_be_zero(self):
        self.store.add(make_transaction(type="income", amount=100, date="2024-01-01"))
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="x"))
        self.assertEqual(self._summary()["balance"], 0)

    def test_only_includes_current_month(self):
        self.store.add(make_transaction(type="income", amount=500, date="2024-01-01"))
        self.store.add(make_transaction(type="income", amount=300, date="2024-02-01"))
        self.assertEqual(self._summary(month="2024-01")["income"], 500)
        self.assertEqual(self._summary(month="2024-02")["income"], 300)

    def test_default_month_is_today(self):
        today = date.today().isoformat()
        self.store.add(make_transaction(type="income", amount=999, date=today))
        s = make_analyzer(self.store).summary()  # no month argument
        self.assertEqual(s["income"], 999)

    def test_future_month_returns_zeros(self):
        self.store.add(make_transaction(type="income", amount=500, date="2024-01-01"))
        s = self._summary(month="2099-12")
        self.assertEqual(s["income"], 0)

    def test_keys_always_present(self):
        s = self._summary()
        for key in ["income", "expenses", "balance", "expenses_by_category"]:
            self.assertIn(key, s)


class TestAnalyzerSummaryCategories(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.store = make_store(self.tmp)

    def test_expenses_grouped_by_category(self):
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="food"))
        self.store.add(make_transaction(type="expense", amount=50, date="2024-01-02", category="food"))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertAlmostEqual(s["expenses_by_category"]["food"], 150)

    def test_multiple_categories_tracked_separately(self):
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="food"))
        self.store.add(make_transaction(type="expense", amount=200, date="2024-01-01", category="rent"))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertEqual(len(s["expenses_by_category"]), 2)

    def test_income_not_in_expenses_by_category(self):
        self.store.add(make_transaction(type="income", amount=1000, date="2024-01-01", category="salary"))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertNotIn("salary", s["expenses_by_category"])

    def test_category_normalized_to_lowercase(self):
        """Regression: 'Food' and 'food' used to be tracked as separate entries."""
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="Food"))
        self.store.add(make_transaction(type="expense", amount=50, date="2024-01-01", category="food"))
        s = make_analyzer(self.store).summary(month="2024-01")
        # After fix: only one key, total 150
        self.assertEqual(len(s["expenses_by_category"]), 1)
        self.assertAlmostEqual(list(s["expenses_by_category"].values())[0], 150)

    def test_mixed_case_categories_merged(self):
        for cat in ["FOOD", "Food", "fOOd", "food"]:
            self.store.add(make_transaction(type="expense", amount=25, date="2024-01-01", category=cat))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertEqual(len(s["expenses_by_category"]), 1)
        self.assertAlmostEqual(list(s["expenses_by_category"].values())[0], 100)

    def test_expenses_total_equals_sum_of_categories(self):
        cats = [("food", 100), ("rent", 500), ("transport", 80)]
        for cat, amt in cats:
            self.store.add(make_transaction(type="expense", amount=amt, date="2024-01-01", category=cat))
        s = make_analyzer(self.store).summary(month="2024-01")
        cat_total = sum(s["expenses_by_category"].values())
        self.assertAlmostEqual(cat_total, s["expenses"])


class TestAnalyzerByCategory(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.store = make_store(self.tmp)

    def test_empty_returns_empty_list(self):
        result = make_analyzer(self.store).by_category(month="2024-01")
        self.assertEqual(result, [])

    def test_sorted_descending_by_amount(self):
        for cat, amt in [("food", 50), ("rent", 200), ("transport", 80)]:
            self.store.add(make_transaction(type="expense", amount=amt, date="2024-01-01", category=cat))
        result = make_analyzer(self.store).by_category(month="2024-01")
        amounts = [a for _, a in result]
        self.assertEqual(amounts, sorted(amounts, reverse=True))

    def test_returns_list_of_2_tuples(self):
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="food"))
        result = make_analyzer(self.store).by_category(month="2024-01")
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)

    def test_top_category_first(self):
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="food"))
        self.store.add(make_transaction(type="expense", amount=500, date="2024-01-01", category="rent"))
        result = make_analyzer(self.store).by_category(month="2024-01")
        self.assertEqual(result[0][0], "rent")

    def test_excludes_income(self):
        self.store.add(make_transaction(type="income", amount=5000, date="2024-01-01", category="salary"))
        self.assertEqual(make_analyzer(self.store).by_category(month="2024-01"), [])

    def test_default_month_uses_today(self):
        today = date.today().isoformat()
        self.store.add(make_transaction(type="expense", amount=100, date=today, category="food"))
        result = make_analyzer(self.store).by_category()
        self.assertEqual(len(result), 1)

    def test_category_names_are_lowercase(self):
        """Regression: category keys used to preserve original case."""
        self.store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="FOOD"))
        result = make_analyzer(self.store).by_category(month="2024-01")
        self.assertEqual(result[0][0], "food")


class TestAnalyzerMonthlyTotals(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.store = make_store(self.tmp)

    def test_empty_store_returns_empty_list(self):
        self.assertEqual(make_analyzer(self.store).monthly_totals(), [])

    def test_single_month_structure(self):
        self.store.add(make_transaction(type="income", amount=1000, date="2024-01-15"))
        self.store.add(make_transaction(type="expense", amount=200, date="2024-01-20", category="food"))
        totals = make_analyzer(self.store).monthly_totals()
        self.assertEqual(len(totals), 1)
        month, income, expense = totals[0]
        self.assertEqual(month, "2024-01")
        self.assertEqual(income, 1000)
        self.assertEqual(expense, 200)

    def test_multiple_months_sorted_chronologically(self):
        for d in ["2024-03-01", "2024-01-01", "2024-02-01"]:
            self.store.add(make_transaction(date=d))
        months = [t[0] for t in make_analyzer(self.store).monthly_totals()]
        self.assertEqual(months, sorted(months))

    def test_returns_3_tuples(self):
        self.store.add(make_transaction(date="2024-01-01"))
        totals = make_analyzer(self.store).monthly_totals()
        self.assertEqual(len(totals[0]), 3)

    def test_month_key_format_yyyy_mm(self):
        self.store.add(make_transaction(date="2024-12-25"))
        self.assertEqual(make_analyzer(self.store).monthly_totals()[0][0], "2024-12")

    def test_income_only_month(self):
        self.store.add(make_transaction(type="income", amount=1000, date="2024-01-01"))
        _, income, expense = make_analyzer(self.store).monthly_totals()[0]
        self.assertEqual(income, 1000)
        self.assertEqual(expense, 0)

    def test_expense_only_month(self):
        self.store.add(make_transaction(type="expense", amount=300, date="2024-01-01", category="x"))
        _, income, expense = make_analyzer(self.store).monthly_totals()[0]
        self.assertEqual(income, 0)
        self.assertEqual(expense, 300)

    def test_multiple_transactions_same_month_aggregated(self):
        for amt in [100, 200, 300]:
            self.store.add(make_transaction(type="income", amount=amt, date="2024-01-01"))
        _, income, _ = make_analyzer(self.store).monthly_totals()[0]
        self.assertEqual(income, 600)

    def test_different_months_separate_entries(self):
        self.store.add(make_transaction(date="2024-01-01"))
        self.store.add(make_transaction(date="2024-02-01"))
        self.assertEqual(len(make_analyzer(self.store).monthly_totals()), 2)

    def test_invariant_totals_across_all_months(self):
        """Sum of all monthly totals should equal overall store totals."""
        for d, amt, tp in [
            ("2024-01-01", 1000, "income"),
            ("2024-01-15", 200, "expense"),
            ("2024-02-01", 500, "income"),
            ("2024-02-10", 100, "expense"),
        ]:
            self.store.add(make_transaction(type=tp, amount=amt, date=d,
                                            category="x" if tp == "expense" else "salary"))
        totals = make_analyzer(self.store).monthly_totals()
        total_income = sum(t[1] for t in totals)
        total_expense = sum(t[2] for t in totals)
        self.assertEqual(total_income, 1500)
        self.assertEqual(total_expense, 300)


class TestAnalyzerFloatingPoint(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.store = make_store(self.tmp)

    def test_many_small_amounts_sum_accurately(self):
        """Adding 100 × 0.10 should equal 10.00 (within float tolerance)."""
        for _ in range(100):
            self.store.add(make_transaction(type="expense", amount=0.10,
                                            date="2024-01-01", category="misc"))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertAlmostEqual(s["expenses"], 10.0, places=5)

    def test_income_expense_balance_consistent(self):
        self.store.add(make_transaction(type="income", amount=1234.56, date="2024-01-01"))
        self.store.add(make_transaction(type="expense", amount=567.89, date="2024-01-01", category="x"))
        s = make_analyzer(self.store).summary(month="2024-01")
        self.assertAlmostEqual(s["balance"], s["income"] - s["expenses"], places=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
