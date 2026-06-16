"""
Tests for budget.py
Covers: set/get, validation, case normalization, persistence, corruption recovery.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from budget import BudgetManager
from helpers import TempDirTest, make_budget


class TestBudgetInit(TempDirTest, unittest.TestCase):

    def test_creates_json_file(self):
        fp = os.path.join(self.tmp, "b.json")
        BudgetManager(filepath=fp)
        self.assertTrue(os.path.exists(fp))

    def test_starts_empty(self):
        self.assertEqual(make_budget(self.tmp).budgets, {})

    def test_custom_filepath_stored(self):
        fp = os.path.join(self.tmp, "b.json")
        b = BudgetManager(filepath=fp)
        self.assertEqual(b.filepath, fp)

    def test_created_file_is_valid_json(self):
        fp = os.path.join(self.tmp, "b.json")
        BudgetManager(filepath=fp)
        with open(fp) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)


class TestBudgetSetGet(TempDirTest, unittest.TestCase):

    def test_set_and_get_basic(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 500)
        self.assertEqual(b.get_budget("food"), 500.0)

    def test_get_unknown_returns_none(self):
        b = make_budget(self.tmp)
        self.assertIsNone(b.get_budget("unknown"))

    def test_set_stores_as_float(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 300)
        self.assertIsInstance(b.get_budget("food"), float)

    def test_set_float_value(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 99.99)
        self.assertAlmostEqual(b.get_budget("food"), 99.99)

    def test_set_normalizes_key_to_lowercase(self):
        b = make_budget(self.tmp)
        b.set_budget("Food", 300)
        self.assertEqual(b.get_budget("food"), 300.0)

    def test_get_normalizes_key_to_lowercase(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 300)
        self.assertEqual(b.get_budget("FOOD"), 300.0)
        self.assertEqual(b.get_budget("Food"), 300.0)

    def test_raw_json_key_is_lowercase(self):
        b = make_budget(self.tmp)
        b.set_budget("Transport", 200)
        with open(b.filepath) as f:
            data = json.load(f)
        self.assertIn("transport", data)
        self.assertNotIn("Transport", data)

    def test_overwrite_budget(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 300)
        b.set_budget("food", 600)
        self.assertEqual(b.get_budget("food"), 600.0)

    def test_multiple_categories_independent(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 300)
        b.set_budget("transport", 100)
        b.set_budget("rent", 1500)
        self.assertEqual(b.get_budget("food"), 300.0)
        self.assertEqual(b.get_budget("transport"), 100.0)
        self.assertEqual(b.get_budget("rent"), 1500.0)

    def test_large_budget(self):
        b = make_budget(self.tmp)
        b.set_budget("rent", 9_999_999.0)
        self.assertAlmostEqual(b.get_budget("rent"), 9_999_999.0)


class TestBudgetValidation(TempDirTest, unittest.TestCase):

    def test_negative_limit_raises(self):
        """Regression: BudgetManager used to accept negative limits silently."""
        b = make_budget(self.tmp)
        with self.assertRaises(ValueError):
            b.set_budget("food", -100)

    def test_zero_limit_raises(self):
        """Regression: BudgetManager used to accept zero limit silently."""
        b = make_budget(self.tmp)
        with self.assertRaises(ValueError):
            b.set_budget("food", 0)

    def test_empty_category_raises(self):
        """Regression: BudgetManager used to accept empty category silently."""
        b = make_budget(self.tmp)
        with self.assertRaises(ValueError):
            b.set_budget("", 100)

    def test_error_message_mentions_positive(self):
        b = make_budget(self.tmp)
        with self.assertRaises(ValueError) as ctx:
            b.set_budget("food", -50)
        self.assertIn("positive", str(ctx.exception).lower())

    def test_error_message_mentions_category(self):
        b = make_budget(self.tmp)
        with self.assertRaises(ValueError) as ctx:
            b.set_budget("", 100)
        self.assertIn("category", str(ctx.exception).lower())

    def test_rejected_budget_not_stored(self):
        b = make_budget(self.tmp)
        try:
            b.set_budget("food", -100)
        except ValueError:
            pass
        self.assertIsNone(b.get_budget("food"))

    def test_small_positive_accepted(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 0.01)
        self.assertAlmostEqual(b.get_budget("food"), 0.01)


class TestBudgetPersistence(TempDirTest, unittest.TestCase):

    def test_persists_after_set(self):
        fp = os.path.join(self.tmp, "b.json")
        b1 = BudgetManager(filepath=fp)
        b1.set_budget("food", 400)
        b2 = BudgetManager(filepath=fp)
        self.assertEqual(b2.get_budget("food"), 400.0)

    def test_multiple_categories_persist(self):
        fp = os.path.join(self.tmp, "b.json")
        b1 = BudgetManager(filepath=fp)
        b1.set_budget("food", 300)
        b1.set_budget("rent", 1500)
        b2 = BudgetManager(filepath=fp)
        self.assertEqual(b2.get_budget("food"), 300.0)
        self.assertEqual(b2.get_budget("rent"), 1500.0)

    def test_overwrite_persists(self):
        fp = os.path.join(self.tmp, "b.json")
        b1 = BudgetManager(filepath=fp)
        b1.set_budget("food", 300)
        b1.set_budget("food", 999)
        b2 = BudgetManager(filepath=fp)
        self.assertEqual(b2.get_budget("food"), 999.0)

    def test_json_file_valid_after_set(self):
        b = make_budget(self.tmp)
        b.set_budget("food", 200)
        with open(b.filepath) as f:
            data = json.load(f)
        self.assertAlmostEqual(data["food"], 200.0)

    def test_multiple_instances_see_same_data(self):
        fp = os.path.join(self.tmp, "b.json")
        b1 = BudgetManager(filepath=fp)
        b1.set_budget("food", 500)
        b2 = BudgetManager(filepath=fp)
        b3 = BudgetManager(filepath=fp)
        self.assertEqual(b2.get_budget("food"), 500.0)
        self.assertEqual(b3.get_budget("food"), 500.0)


class TestBudgetCorruption(TempDirTest, unittest.TestCase):

    def test_corrupted_json_does_not_crash(self):
        """Regression: load() used to raise JSONDecodeError on corrupted file."""
        fp = os.path.join(self.tmp, "b.json")
        with open(fp, "w") as f:
            f.write("NOT VALID JSON {{{")
        try:
            b = BudgetManager(filepath=fp)
            # If it recovers gracefully, budgets should be empty
            self.assertEqual(b.budgets, {})
        except Exception as e:
            self.fail(f"BudgetManager raised {type(e).__name__} on corrupted file: {e}")

    def test_corrupted_file_is_replaced(self):
        """After corruption recovery, file should be valid JSON."""
        fp = os.path.join(self.tmp, "b.json")
        with open(fp, "w") as f:
            f.write("{bad json")
        BudgetManager(filepath=fp)
        with open(fp) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_empty_file_handled(self):
        fp = os.path.join(self.tmp, "b.json")
        with open(fp, "w") as f:
            f.write("")
        try:
            b = BudgetManager(filepath=fp)
            self.assertIsInstance(b.budgets, dict)
        except Exception as e:
            self.fail(f"Empty file raised {type(e).__name__}: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
