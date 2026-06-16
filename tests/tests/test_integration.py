"""
Integration tests — full end-to-end workflows across all modules.
Covers: multi-step workflows, cross-module state, data consistency invariants.
"""
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import Analyzer
from budget import BudgetManager
from helpers import TempDirTest, capture, make_handler, make_store, make_transaction
from store import TransactionStore
from transaction import Transaction


TODAY = date.today().isoformat()
THIS_MONTH = date.today().strftime("%Y-%m")


class TestAddListDeleteWorkflow(TempDirTest, unittest.TestCase):

    def test_add_list_delete_cycle(self):
        h = make_handler(self.tmp)
        capture(h, "add income 1000 salary Pay")
        out = capture(h, "list")
        self.assertIn("salary", out)
        capture(h, "delete 1")
        self.assertEqual(capture(h, "list"), "")

    def test_multiple_adds_then_selective_delete(self):
        h = make_handler(self.tmp)
        for cat in ["salary", "bonus", "freelance"]:
            capture(h, f"add income 100 {cat} Pay")
        capture(h, "delete 2")
        out = capture(h, "list")
        self.assertIn("salary", out)
        self.assertNotIn("bonus", out)
        self.assertIn("freelance", out)

    def test_add_delete_add_id_sequence(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay")   # id=1
        capture(h, "add income 100 bonus Pay")    # id=2
        capture(h, "delete 2")
        capture(h, "add income 100 gift Pay")     # id=2 again (next_id after max=1)
        ids = [t.id for t in h.store.transactions]
        self.assertIn(1, ids)
        self.assertIn(2, ids)


class TestBudgetSummaryWorkflow(TempDirTest, unittest.TestCase):

    def test_set_budget_then_check_summary_under(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 200 food Groceries --date {TODAY}")
        capture(h, "budget food 500")
        out = capture(h, "summary")
        self.assertIn("under budget", out)

    def test_set_budget_then_check_summary_over(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 600 food Groceries --date {TODAY}")
        capture(h, "budget food 500")
        out = capture(h, "summary")
        self.assertIn("over budget", out)

    def test_budget_overwrite_reflects_in_summary(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 400 food Groceries --date {TODAY}")
        capture(h, "budget food 300")
        out1 = capture(h, "summary")
        self.assertIn("over budget", out1)
        capture(h, "budget food 500")
        out2 = capture(h, "summary")
        self.assertIn("under budget", out2)

    def test_multiple_categories_budget_status(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 100 food Lunch --date {TODAY}")
        capture(h, f"add expense 200 rent Rent --date {TODAY}")
        capture(h, "budget food 500")
        capture(h, "budget rent 100")
        out = capture(h, "summary")
        self.assertIn("under budget", out)   # food
        self.assertIn("over budget", out)    # rent


class TestPersistenceAcrossRestarts(TempDirTest, unittest.TestCase):

    def test_transactions_survive_restart(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(type="income", amount=500, category="salary"))
        s1.add(make_transaction(type="expense", amount=200, category="food"))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(len(s2.transactions), 2)

    def test_budgets_survive_restart(self):
        fp = os.path.join(self.tmp, "b.json")
        b1 = BudgetManager(filepath=fp)
        b1.set_budget("food", 300)
        b2 = BudgetManager(filepath=fp)
        self.assertEqual(b2.get_budget("food"), 300.0)

    def test_analyzer_works_on_reloaded_store(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(type="income", amount=1000, date="2024-01-01"))
        s1.add(make_transaction(type="expense", amount=300, date="2024-01-01", category="food"))
        s2 = TransactionStore(filepath=fp)
        summary = Analyzer(s2).summary(month="2024-01")
        self.assertEqual(summary["income"], 1000)
        self.assertEqual(summary["expenses"], 300)
        self.assertEqual(summary["balance"], 700)


class TestDataConsistencyInvariants(TempDirTest, unittest.TestCase):

    def test_summary_income_equals_sum_of_income_transactions(self):
        store = make_store(self.tmp)
        amounts = [100, 250, 500, 75]
        for amt in amounts:
            store.add(make_transaction(type="income", amount=amt, date="2024-01-01"))
        s = Analyzer(store).summary(month="2024-01")
        self.assertAlmostEqual(s["income"], sum(amounts))

    def test_summary_expenses_equals_sum_of_expense_transactions(self):
        store = make_store(self.tmp)
        amounts = [50, 120, 200]
        for amt in amounts:
            store.add(make_transaction(type="expense", amount=amt, date="2024-01-01", category="x"))
        s = Analyzer(store).summary(month="2024-01")
        self.assertAlmostEqual(s["expenses"], sum(amounts))

    def test_balance_always_income_minus_expenses(self):
        store = make_store(self.tmp)
        store.add(make_transaction(type="income", amount=3000, date="2024-01-01"))
        store.add(make_transaction(type="expense", amount=1200, date="2024-01-01", category="x"))
        store.add(make_transaction(type="expense", amount=300, date="2024-01-01", category="y"))
        s = Analyzer(store).summary(month="2024-01")
        self.assertAlmostEqual(s["balance"], s["income"] - s["expenses"])

    def test_by_category_amounts_sum_to_total_expenses(self):
        store = make_store(self.tmp)
        for cat, amt in [("food", 100), ("rent", 500), ("transport", 80)]:
            store.add(make_transaction(type="expense", amount=amt, date="2024-01-01", category=cat))
        a = Analyzer(store)
        s = a.summary(month="2024-01")
        cat_sum = sum(amt for _, amt in a.by_category(month="2024-01"))
        self.assertAlmostEqual(cat_sum, s["expenses"])

    def test_monthly_totals_sum_matches_all_transactions(self):
        store = make_store(self.tmp)
        for d, amt, tp in [
            ("2024-01-01", 1000, "income"),
            ("2024-01-10", 200, "expense"),
            ("2024-02-01", 800, "income"),
            ("2024-02-15", 150, "expense"),
        ]:
            store.add(make_transaction(type=tp, amount=amt, date=d,
                                       category="x" if tp == "expense" else "s"))
        totals = Analyzer(store).monthly_totals()
        total_income = sum(t[1] for t in totals)
        total_expense = sum(t[2] for t in totals)
        all_income = sum(t.amount for t in store.transactions if t.type == "income")
        all_expense = sum(t.amount for t in store.transactions if t.type == "expense")
        self.assertAlmostEqual(total_income, all_income)
        self.assertAlmostEqual(total_expense, all_expense)

    def test_store_count_consistent_after_add_delete_cycles(self):
        store = make_store(self.tmp)
        for _ in range(10):
            store.add(make_transaction())
        for id_ in range(1, 6):
            store.delete(id_)
        self.assertEqual(len(store.transactions), 5)

    def test_store_ids_unique_after_sequential_adds(self):
        store = make_store(self.tmp)
        for _ in range(20):
            store.add(make_transaction())
        ids = [t.id for t in store.transactions]
        self.assertEqual(len(ids), len(set(ids)))


class TestCategoryNormalizationEndToEnd(TempDirTest, unittest.TestCase):

    def test_filter_and_summary_use_consistent_casing(self):
        """
        Regression: before the fix, filter() was case-insensitive but
        summary() tracked categories with original casing — so filtered
        results and summary categories could be out of sync.
        """
        store = make_store(self.tmp)
        store.add(make_transaction(type="expense", amount=100, date="2024-01-01", category="Food"))
        store.add(make_transaction(type="expense", amount=50, date="2024-01-01", category="food"))
        store.add(make_transaction(type="expense", amount=25, date="2024-01-01", category="FOOD"))
        a = Analyzer(store)
        s = a.summary(month="2024-01")
        # All three should merge into one lowercase key
        self.assertEqual(len(s["expenses_by_category"]), 1)
        self.assertAlmostEqual(s["expenses_by_category"]["food"], 175)
        # Filter should agree
        filtered = store.filter(category="food")
        self.assertEqual(len(filtered), 3)

    def test_export_then_reimport_preserves_data(self):
        """Data exported to CSV then re-imported via a new store stays intact."""
        import tempfile
        store = make_store(self.tmp)
        store.add(make_transaction(type="income", amount=500, category="salary", date="2024-01-01"))
        store.add(make_transaction(type="expense", amount=200, category="food", date="2024-01-10"))
        os.chdir(self.tmp)
        export_file, count = store.export()
        self.assertEqual(count, 2)
        # The export file is a plain CSV — verify it can be read back
        fp2 = os.path.join(self.tmp, "imported.csv")
        import csv, shutil
        shutil.copy(export_file, fp2)
        store2 = TransactionStore(filepath=fp2)
        self.assertEqual(len(store2.transactions), 2)
        amounts = sorted(t.amount for t in store2.transactions)
        self.assertEqual(amounts, [200, 500])


if __name__ == "__main__":
    unittest.main(verbosity=2)
