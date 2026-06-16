"""
Tests for store.py
Covers: CRUD, persistence, filtering, export, CSV quoting, corruption recovery,
        duplicate-ID guard, idempotency, state isolation.
"""
import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import TempDirTest, make_store, make_transaction
from store import TransactionStore
from transaction import Transaction


class TestStoreInit(TempDirTest, unittest.TestCase):

    def test_creates_csv_file_on_first_run(self):
        fp = os.path.join(self.tmp, "new.csv")
        TransactionStore(filepath=fp)
        self.assertTrue(os.path.exists(fp))

    def test_new_store_is_empty(self):
        self.assertEqual(make_store(self.tmp).transactions, [])

    def test_custom_filepath_stored(self):
        fp = os.path.join(self.tmp, "custom.csv")
        s = TransactionStore(filepath=fp)
        self.assertEqual(s.filepath, fp)

    def test_csv_file_has_header(self):
        fp = os.path.join(self.tmp, "tx.csv")
        TransactionStore(filepath=fp)
        with open(fp) as f:
            header = f.readline()
        self.assertIn("id", header)
        self.assertIn("type", header)
        self.assertIn("amount", header)


class TestStoreAdd(TempDirTest, unittest.TestCase):

    def test_add_increases_count(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        self.assertEqual(len(s.transactions), 1)

    def test_add_assigns_id_1_to_first(self):
        s = make_store(self.tmp)
        t = make_transaction()
        s.add(t)
        self.assertEqual(t.id, 1)

    def test_add_increments_ids_sequentially(self):
        s = make_store(self.tmp)
        t1, t2, t3 = make_transaction(), make_transaction(), make_transaction()
        s.add(t1); s.add(t2); s.add(t3)
        self.assertEqual([t1.id, t2.id, t3.id], [1, 2, 3])

    def test_add_does_not_overwrite_preset_id(self):
        s = make_store(self.tmp)
        t = make_transaction(id=50)
        s.add(t)
        self.assertEqual(t.id, 50)

    def test_add_duplicate_preset_id_raises(self):
        """Regression: store used to silently accept duplicate IDs."""
        s = make_store(self.tmp)
        s.add(make_transaction(id=1))
        with self.assertRaises(ValueError):
            s.add(make_transaction(id=1))

    def test_add_persists_immediately(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(amount=250.0))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(len(s2.transactions), 1)
        self.assertAlmostEqual(s2.transactions[0].amount, 250.0)

    def test_add_income_type_preserved(self):
        s = make_store(self.tmp)
        s.add(make_transaction(type="income"))
        self.assertEqual(s.transactions[0].type, "income")

    def test_add_expense_type_preserved(self):
        s = make_store(self.tmp)
        s.add(make_transaction(type="expense"))
        self.assertEqual(s.transactions[0].type, "expense")

    def test_add_preserves_all_fields(self):
        s = make_store(self.tmp)
        t = make_transaction(type="expense", amount=99.9, category="food",
                             date="2024-06-01", description="Lunch")
        s.add(t)
        stored = s.transactions[0]
        self.assertEqual(stored.type, "expense")
        self.assertAlmostEqual(stored.amount, 99.9)
        self.assertEqual(stored.category, "food")
        self.assertEqual(stored.date, "2024-06-01")
        self.assertEqual(stored.description, "Lunch")

    def test_add_description_with_pipe_character(self):
        """Regression: pipe in description used to corrupt the CSV."""
        s = make_store(self.tmp)
        t = make_transaction(description="Pizza|pasta|salad")
        s.add(t)
        fp = os.path.join(self.tmp, "tx.csv")
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(len(s2.transactions), 1)
        self.assertEqual(s2.transactions[0].description, "Pizza|pasta|salad")

    def test_add_description_with_multiple_pipes(self):
        s = make_store(self.tmp)
        t = make_transaction(description="a|b|c|d|e")
        s.add(t)
        fp = os.path.join(self.tmp, "tx.csv")
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, "a|b|c|d|e")

    def test_add_description_with_quotes(self):
        s = make_store(self.tmp)
        t = make_transaction(description='He said "hello"')
        s.add(t)
        fp = os.path.join(self.tmp, "tx.csv")
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].description, 'He said "hello"')


class TestStoreDelete(TempDirTest, unittest.TestCase):

    def test_delete_existing_returns_true(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        self.assertTrue(s.delete(1))

    def test_delete_removes_from_list(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        s.delete(1)
        self.assertEqual(len(s.transactions), 0)

    def test_delete_nonexistent_returns_false(self):
        s = make_store(self.tmp)
        self.assertFalse(s.delete(999))

    def test_delete_persists(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction())
        s1.delete(1)
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(len(s2.transactions), 0)

    def test_delete_removes_correct_record(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="salary"))
        s.add(make_transaction(category="bonus"))
        s.delete(1)
        self.assertEqual(s.transactions[0].category, "bonus")

    def test_delete_from_empty_store(self):
        s = make_store(self.tmp)
        self.assertFalse(s.delete(1))

    def test_delete_is_idempotent_on_missing_id(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        s.delete(1)
        # Second delete of same id should just return False, not crash
        self.assertFalse(s.delete(1))

    def test_delete_middle_item(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="a"))
        s.add(make_transaction(category="b"))
        s.add(make_transaction(category="c"))
        s.delete(2)
        categories = [t.category for t in s.transactions]
        self.assertNotIn("b", categories)
        self.assertIn("a", categories)
        self.assertIn("c", categories)


class TestStoreNextId(TempDirTest, unittest.TestCase):

    def test_empty_store_returns_1(self):
        self.assertEqual(make_store(self.tmp).next_id(), 1)

    def test_after_one_add(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        self.assertEqual(s.next_id(), 2)

    def test_uses_max_not_count(self):
        s = make_store(self.tmp)
        s.add(make_transaction(id=100))
        s.add(make_transaction(id=3))
        self.assertEqual(s.next_id(), 101)

    def test_after_delete_uses_remaining_max(self):
        s = make_store(self.tmp)
        s.add(make_transaction())  # id=1
        s.add(make_transaction())  # id=2
        s.delete(2)
        self.assertEqual(s.next_id(), 2)  # max remaining is 1, so next is 2

    def test_after_all_deleted_resets_to_1(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        s.delete(1)
        self.assertEqual(s.next_id(), 1)


class TestStoreListTransactions(TempDirTest, unittest.TestCase):

    def test_empty_store_returns_empty_list(self):
        self.assertEqual(make_store(self.tmp).list_transactions(), [])

    def test_returns_all_transactions(self):
        s = make_store(self.tmp)
        s.add(make_transaction()); s.add(make_transaction())
        self.assertEqual(len(s.list_transactions()), 2)

    def test_sorted_descending_by_date(self):
        s = make_store(self.tmp)
        for date in ["2024-01-01", "2024-03-15", "2024-02-10"]:
            s.add(make_transaction(date=date))
        dates = [t.date for t in s.list_transactions()]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_category_filter(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="food"))
        s.add(make_transaction(category="salary"))
        result = s.list_transactions(category="food")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].category, "food")

    def test_category_filter_case_insensitive(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="Food"))
        self.assertEqual(len(s.list_transactions(category="food")), 1)
        self.assertEqual(len(s.list_transactions(category="FOOD")), 1)

    def test_category_filter_no_match(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="salary"))
        self.assertEqual(s.list_transactions(category="xyz"), [])

    def test_sort_stability_same_date(self):
        """Multiple transactions on same date should all be returned."""
        s = make_store(self.tmp)
        for _ in range(3):
            s.add(make_transaction(date="2024-01-01"))
        self.assertEqual(len(s.list_transactions()), 3)


class TestStoreFilter(TempDirTest, unittest.TestCase):

    def test_filter_by_month(self):
        s = make_store(self.tmp)
        s.add(make_transaction(date="2024-01-10"))
        s.add(make_transaction(date="2024-02-05"))
        result = s.filter(month="2024-01")
        self.assertEqual(len(result), 1)

    def test_filter_by_category(self):
        s = make_store(self.tmp)
        s.add(make_transaction(category="food"))
        s.add(make_transaction(category="rent"))
        self.assertEqual(len(s.filter(category="food")), 1)

    def test_filter_month_and_category_combined(self):
        s = make_store(self.tmp)
        s.add(make_transaction(date="2024-01-01", category="food"))
        s.add(make_transaction(date="2024-01-01", category="rent"))
        s.add(make_transaction(date="2024-02-01", category="food"))
        self.assertEqual(len(s.filter(month="2024-01", category="food")), 1)

    def test_filter_no_args_returns_all(self):
        s = make_store(self.tmp)
        s.add(make_transaction()); s.add(make_transaction())
        self.assertEqual(len(s.filter()), 2)

    def test_filter_no_match_returns_empty(self):
        s = make_store(self.tmp)
        s.add(make_transaction(date="2024-01-01"))
        self.assertEqual(s.filter(month="2025-12"), [])

    def test_filter_does_not_mutate_store(self):
        s = make_store(self.tmp)
        s.add(make_transaction()); s.add(make_transaction())
        _ = s.filter(category="xyz")
        self.assertEqual(len(s.transactions), 2)


class TestStoreExport(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        os.chdir(self.tmp)

    def test_export_all_returns_correct_filename(self):
        s = make_store(self.tmp)
        filename, _ = s.export()
        self.assertEqual(filename, "export_all.csv")

    def test_export_all_returns_correct_count(self):
        s = make_store(self.tmp)
        s.add(make_transaction()); s.add(make_transaction())
        _, count = s.export()
        self.assertEqual(count, 2)

    def test_export_all_creates_file(self):
        s = make_store(self.tmp)
        filename, _ = s.export()
        self.assertTrue(os.path.exists(filename))

    def test_export_by_month_filename(self):
        s = make_store(self.tmp)
        filename, _ = s.export(month="2024-03")
        self.assertEqual(filename, "export_2024-03.csv")

    def test_export_by_month_filters_correctly(self):
        s = make_store(self.tmp)
        s.add(make_transaction(date="2024-01-10"))
        s.add(make_transaction(date="2024-02-05"))
        _, count = s.export(month="2024-01")
        self.assertEqual(count, 1)

    def test_export_empty_store(self):
        s = make_store(self.tmp)
        _, count = s.export()
        self.assertEqual(count, 0)

    def test_export_file_has_correct_header(self):
        s = make_store(self.tmp)
        s.add(make_transaction())
        filename, _ = s.export()
        with open(filename) as f:
            header = f.readline()
        for field in ["id", "type", "amount", "category", "date", "description"]:
            self.assertIn(field, header)


class TestStoreCorruption(TempDirTest, unittest.TestCase):

    def test_garbage_file_starts_empty(self):
        fp = os.path.join(self.tmp, "tx.csv")
        with open(fp, "w") as f:
            f.write("GARBAGE\nDATA\n")
        s = TransactionStore(filepath=fp)
        self.assertEqual(s.transactions, [])

    def test_corrupted_file_is_overwritten(self):
        """Regression: corrupted file used to persist across restarts."""
        fp = os.path.join(self.tmp, "tx.csv")
        with open(fp, "w") as f:
            f.write("GARBAGE\nDATA\n")
        TransactionStore(filepath=fp)
        # Second load should succeed cleanly (no longer corrupted)
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions, [])

    def test_partial_corruption_is_handled(self):
        fp = os.path.join(self.tmp, "tx.csv")
        with open(fp, "w") as f:
            f.write("id|type|amount|category|date|description\n")
            f.write("NOTANINT|badtype|notafloat|cat|baddate|desc\n")
        s = TransactionStore(filepath=fp)
        self.assertEqual(s.transactions, [])


class TestStorePersistenceRoundtrip(TempDirTest, unittest.TestCase):

    def test_full_roundtrip_all_fields(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(Transaction("expense", 55.5, "food", "2024-06-15", "Lunch"))
        s2 = TransactionStore(filepath=fp)
        t = s2.transactions[0]
        self.assertEqual(t.type, "expense")
        self.assertAlmostEqual(t.amount, 55.5)
        self.assertEqual(t.category, "food")
        self.assertEqual(t.date, "2024-06-15")
        self.assertEqual(t.description, "Lunch")

    def test_multiple_transactions_roundtrip(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        for i in range(10):
            s1.add(make_transaction(amount=float(i + 1)))
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(len(s2.transactions), 10)

    def test_ids_survive_reload(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        t = make_transaction()
        s1.add(t)
        original_id = t.id
        s2 = TransactionStore(filepath=fp)
        self.assertEqual(s2.transactions[0].id, original_id)

    def test_amount_precision_survives_reload(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction(amount=19.99))
        s2 = TransactionStore(filepath=fp)
        self.assertAlmostEqual(s2.transactions[0].amount, 19.99, places=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
