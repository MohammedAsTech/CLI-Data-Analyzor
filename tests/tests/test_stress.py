"""
Stress and performance tests.
Covers: large datasets, rapid cycles, long strings, many categories,
        reload performance, filter accuracy at scale.
"""
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import Analyzer
from helpers import TempDirTest, make_store, make_transaction
from store import TransactionStore
from transaction import Transaction


FAST_THRESHOLD_S = 2.0   # any single operation should complete in under 2 s


class TestLargeDataset(TempDirTest, unittest.TestCase):

    def test_add_1000_transactions(self):
        store = make_store(self.tmp)
        for i in range(1000):
            store.add(make_transaction(amount=float(i + 1)))
        self.assertEqual(len(store.transactions), 1000)

    def test_reload_1000_transactions(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        for i in range(1000):
            s1.add(make_transaction(amount=float(i + 1)))
        start = time.monotonic()
        s2 = TransactionStore(filepath=fp)
        elapsed = time.monotonic() - start
        self.assertEqual(len(s2.transactions), 1000)
        self.assertLess(elapsed, FAST_THRESHOLD_S,
                        f"Reload of 1000 transactions took {elapsed:.2f}s")

    def test_summary_over_large_dataset(self):
        store = make_store(self.tmp)
        for i in range(500):
            store.add(make_transaction(type="income", amount=10.0, date="2024-01-01"))
            store.add(make_transaction(type="expense", amount=5.0, date="2024-01-01", category="food"))
        start = time.monotonic()
        s = Analyzer(store).summary(month="2024-01")
        elapsed = time.monotonic() - start
        self.assertAlmostEqual(s["income"], 5000.0)
        self.assertAlmostEqual(s["expenses"], 2500.0)
        self.assertLess(elapsed, FAST_THRESHOLD_S)

    def test_filter_over_large_dataset_accuracy(self):
        store = make_store(self.tmp)
        for i in range(300):
            store.add(make_transaction(date="2024-01-15", category="food"))
            store.add(make_transaction(date="2024-02-10", category="food"))
            store.add(make_transaction(date="2024-01-20", category="rent"))
        result = store.filter(month="2024-01", category="food")
        self.assertEqual(len(result), 300)

    def test_list_transactions_sorted_correctly_at_scale(self):
        import random
        store = make_store(self.tmp)
        months = ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"]
        days = [f"{d:02d}" for d in range(1, 29)]
        for _ in range(200):
            m = random.choice(months)
            d = random.choice(days)
            store.add(make_transaction(date=f"{m}-{d}"))
        result = store.list_transactions()
        dates = [t.date for t in result]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_monthly_totals_200_months_no_crash(self):
        store = make_store(self.tmp)
        # Span 200 unique months across ~17 years
        for year in range(2000, 2017):
            for month in range(1, 13):
                store.add(make_transaction(date=f"{year}-{month:02d}-01", amount=100.0))
        totals = Analyzer(store).monthly_totals()
        self.assertGreaterEqual(len(totals), 200)

    def test_by_category_100_categories(self):
        store = make_store(self.tmp)
        for i in range(100):
            store.add(make_transaction(type="expense", amount=float(i + 1),
                                       date="2024-01-01", category=f"cat_{i:03d}"))
        result = Analyzer(store).by_category(month="2024-01")
        self.assertEqual(len(result), 100)
        # Verify descending order
        amounts = [a for _, a in result]
        self.assertEqual(amounts, sorted(amounts, reverse=True))


class TestRapidCycles(TempDirTest, unittest.TestCase):

    def test_rapid_add_delete_200_cycles(self):
        """Add then immediately delete a transaction 200 times — store stays consistent."""
        store = make_store(self.tmp)
        for _ in range(200):
            store.add(make_transaction())
            last_id = store.transactions[-1].id
            store.delete(last_id)
        self.assertEqual(len(store.transactions), 0)

    def test_rapid_add_200_then_delete_all(self):
        store = make_store(self.tmp)
        for _ in range(200):
            store.add(make_transaction())
        ids = [t.id for t in store.transactions]
        for id_ in ids:
            store.delete(id_)
        self.assertEqual(len(store.transactions), 0)

    def test_interleaved_add_delete_consistent_ids(self):
        """Interleaving adds and deletes should never produce duplicate IDs."""
        store = make_store(self.tmp)
        for i in range(100):
            store.add(make_transaction())
            if i % 3 == 0 and store.transactions:
                store.delete(store.transactions[0].id)
        ids = [t.id for t in store.transactions]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate IDs found after interleaved operations")


class TestEdgeCaseInputs(TempDirTest, unittest.TestCase):

    def test_very_long_description_stored_and_retrieved(self):
        fp = os.path.join(self.tmp, "tx.csv")
        long_desc = "A" * 5000
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(description=long_desc))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, long_desc)

    def test_description_with_all_special_chars(self):
        fp = os.path.join(self.tmp, "tx.csv")
        special = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(description=special))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, special)

    def test_description_with_pipe_character_roundtrip(self):
        """Regression: pipe in description used to corrupt the CSV delimiter."""
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(description="a|b|c|d|e|f"))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, "a|b|c|d|e|f")

    def test_unicode_in_all_fields_roundtrip(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        t = Transaction("expense", 50.0, "אוכל", "2024-01-01", "ארוחת צהריים")
        s1.add(t)
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].category, "אוכל")
        self.assertEqual(s2.transactions[0].description, "ארוחת צהריים")

    def test_minimum_valid_amount_precision(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(amount=0.01))
        s2 = TransactionStore(filepath=fp)
        self.assertAlmostEqual(s2.transactions[0].amount, 0.01, places=5)

    def test_maximum_practical_amount_roundtrip(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(amount=9_999_999.99))
        s2 = TransactionStore(filepath=fp)
        self.assertAlmostEqual(s2.transactions[0].amount, 9_999_999.99, places=2)

    def test_transaction_with_empty_description_roundtrip(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(description=""))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, "")


class TestPerformanceBenchmarks(TempDirTest, unittest.TestCase):

    def test_1000_adds_under_threshold(self):
        store = make_store(self.tmp)
        start = time.monotonic()
        for i in range(1000):
            store.add(make_transaction(amount=float(i + 1)))
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 30.0,
                        f"1000 sequential adds took {elapsed:.2f}s (too slow)")

    def test_filter_1000_transactions_under_threshold(self):
        store = make_store(self.tmp)
        for i in range(1000):
            cat = "food" if i % 2 == 0 else "rent"
            store.add(make_transaction(category=cat))
        start = time.monotonic()
        result = store.filter(category="food")
        elapsed = time.monotonic() - start
        self.assertEqual(len(result), 500)
        self.assertLess(elapsed, FAST_THRESHOLD_S)

    def test_summary_1000_transactions_under_threshold(self):
        store = make_store(self.tmp)
        for i in range(1000):
            store.add(make_transaction(type="expense", amount=1.0,
                                       date="2024-01-01", category=f"cat_{i % 20}"))
        start = time.monotonic()
        _ = Analyzer(store).summary(month="2024-01")
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, FAST_THRESHOLD_S)


if __name__ == "__main__":
    unittest.main(verbosity=2)
