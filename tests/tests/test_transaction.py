"""
Tests for transaction.py
Covers: validation, boundary values, serialization, error messages.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transaction import Transaction


def _t(**kw):
    defaults = dict(type="income", amount=100.0, category="salary",
                    date="2024-01-15", description="pay")
    defaults.update(kw)
    return Transaction(**defaults)


class TestTransactionValidType(unittest.TestCase):

    def test_income_accepted(self):
        self.assertEqual(_t(type="income").type, "income")

    def test_expense_accepted(self):
        self.assertEqual(_t(type="expense").type, "expense")

    def test_transfer_rejected(self):
        with self.assertRaises(ValueError):
            _t(type="transfer")

    def test_uppercase_income_rejected(self):
        with self.assertRaises(ValueError):
            _t(type="Income")

    def test_uppercase_expense_rejected(self):
        with self.assertRaises(ValueError):
            _t(type="EXPENSE")

    def test_empty_type_rejected(self):
        with self.assertRaises(ValueError):
            _t(type="")

    def test_none_type_rejected(self):
        with self.assertRaises((ValueError, TypeError)):
            _t(type=None)

    def test_whitespace_type_rejected(self):
        with self.assertRaises(ValueError):
            _t(type=" income")

    def test_error_message_mentions_type(self):
        with self.assertRaises(ValueError) as ctx:
            _t(type="bad")
        self.assertIn("income", str(ctx.exception).lower())


class TestTransactionValidAmount(unittest.TestCase):

    def test_positive_float(self):
        self.assertAlmostEqual(_t(amount=99.99).amount, 99.99)

    def test_positive_integer(self):
        self.assertEqual(_t(amount=50).amount, 50)

    def test_minimum_positive(self):
        self.assertAlmostEqual(_t(amount=0.01).amount, 0.01)

    def test_large_amount(self):
        self.assertAlmostEqual(_t(amount=10_000_000.0).amount, 10_000_000.0)

    def test_zero_rejected(self):
        with self.assertRaises(ValueError):
            _t(amount=0)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            _t(amount=-1)

    def test_large_negative_rejected(self):
        with self.assertRaises(ValueError):
            _t(amount=-999999)

    def test_float_zero_rejected(self):
        with self.assertRaises(ValueError):
            _t(amount=0.0)

    def test_error_message_mentions_positive(self):
        with self.assertRaises(ValueError) as ctx:
            _t(amount=-5)
        self.assertIn("positive", str(ctx.exception).lower())


class TestTransactionValidCategory(unittest.TestCase):

    def test_simple_string(self):
        self.assertEqual(_t(category="food").category, "food")

    def test_category_with_spaces(self):
        self.assertEqual(_t(category="my salary").category, "my salary")

    def test_unicode_category(self):
        self.assertEqual(_t(category="אוכל").category, "אוכל")

    def test_numeric_string_category(self):
        self.assertEqual(_t(category="123").category, "123")

    def test_empty_string_rejected(self):
        with self.assertRaises(ValueError):
            _t(category="")

    def test_none_category_rejected(self):
        with self.assertRaises((ValueError, TypeError)):
            _t(category=None)

    def test_error_message_mentions_category(self):
        with self.assertRaises(ValueError) as ctx:
            _t(category="")
        self.assertIn("category", str(ctx.exception).lower())


class TestTransactionValidDate(unittest.TestCase):

    def test_standard_date(self):
        self.assertEqual(_t(date="2024-06-15").date, "2024-06-15")

    def test_year_2000(self):
        self.assertEqual(_t(date="2000-01-01").date, "2000-01-01")

    def test_far_future(self):
        self.assertEqual(_t(date="2099-12-31").date, "2099-12-31")

    def test_leap_day(self):
        self.assertEqual(_t(date="2024-02-29").date, "2024-02-29")

    def test_slash_separator_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="2024/01/15")

    def test_reversed_format_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="15-01-2024")

    def test_month_only_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="2024-01")

    def test_day_32_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="2024-01-32")

    def test_month_13_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="2024-13-01")

    def test_invalid_leap_day_rejected(self):
        with self.assertRaises(ValueError):
            _t(date="2023-02-29")  # 2023 is not a leap year


class TestTransactionDescription(unittest.TestCase):

    def test_normal_description(self):
        self.assertEqual(_t(description="Monthly pay").description, "Monthly pay")

    def test_empty_description_accepted(self):
        self.assertEqual(_t(description="").description, "")

    def test_none_description_accepted(self):
        # No validation on description
        self.assertIsNone(_t(description=None).description)

    def test_unicode_description(self):
        self.assertEqual(_t(description="שלום עולם").description, "שלום עולם")

    def test_very_long_description(self):
        long = "x" * 10_000
        self.assertEqual(_t(description=long).description, long)


class TestTransactionId(unittest.TestCase):

    def test_default_id_is_none(self):
        self.assertIsNone(_t().id)

    def test_explicit_id_stored(self):
        self.assertEqual(_t(id=42).id, 42)

    def test_id_zero(self):
        self.assertEqual(_t(id=0).id, 0)

    def test_id_large(self):
        self.assertEqual(_t(id=999_999).id, 999_999)


class TestTransactionToDict(unittest.TestCase):

    def test_all_keys_present(self):
        d = _t().to_dict()
        self.assertEqual(set(d), {"id", "type", "amount", "category", "date", "description"})

    def test_values_match_attributes(self):
        t = Transaction("expense", 55.5, "food", "2024-03-10", "Lunch", id=7)
        d = t.to_dict()
        self.assertEqual(d["id"], 7)
        self.assertEqual(d["type"], "expense")
        self.assertAlmostEqual(d["amount"], 55.5)
        self.assertEqual(d["category"], "food")
        self.assertEqual(d["date"], "2024-03-10")
        self.assertEqual(d["description"], "Lunch")

    def test_returns_independent_copies(self):
        t = _t()
        d1, d2 = t.to_dict(), t.to_dict()
        self.assertIsNot(d1, d2)

    def test_mutating_dict_does_not_affect_transaction(self):
        t = _t(category="salary")
        d = t.to_dict()
        d["category"] = "hacked"
        self.assertEqual(t.category, "salary")


class TestTransactionFromDict(unittest.TestCase):

    def _base(self, **kw):
        d = {"id": "1", "type": "income", "amount": "200.0",
             "category": "salary", "date": "2024-01-01", "description": "Pay"}
        d.update(kw)
        return d

    def test_basic_roundtrip(self):
        t = Transaction.from_dict(self._base())
        self.assertEqual(t.id, 1)
        self.assertAlmostEqual(t.amount, 200.0)

    def test_expense_roundtrip(self):
        t = Transaction.from_dict(self._base(type="expense", amount="75.25", id="9"))
        self.assertEqual(t.type, "expense")
        self.assertEqual(t.id, 9)

    def test_missing_id_raises_key_error(self):
        d = self._base()
        del d["id"]
        with self.assertRaises(KeyError):
            Transaction.from_dict(d)

    def test_missing_type_raises_key_error(self):
        d = self._base()
        del d["type"]
        with self.assertRaises(KeyError):
            Transaction.from_dict(d)

    def test_missing_amount_raises_key_error(self):
        d = self._base()
        del d["amount"]
        with self.assertRaises(KeyError):
            Transaction.from_dict(d)

    def test_missing_category_raises_key_error(self):
        d = self._base()
        del d["category"]
        with self.assertRaises(KeyError):
            Transaction.from_dict(d)

    def test_missing_date_raises_key_error(self):
        d = self._base()
        del d["date"]
        with self.assertRaises(KeyError):
            Transaction.from_dict(d)

    def test_nonnumeric_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            Transaction.from_dict(self._base(amount="abc"))

    def test_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            Transaction.from_dict(self._base(amount="-10"))

    def test_invalid_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            Transaction.from_dict(self._base(type="transfer"))

    def test_key_error_has_helpful_message(self):
        d = self._base()
        del d["amount"]
        with self.assertRaises(KeyError) as ctx:
            Transaction.from_dict(d)
        self.assertIn("amount", str(ctx.exception))

    def test_full_roundtrip_via_dicts(self):
        original = Transaction("expense", 77.7, "food", "2024-05-20", "Dinner", id=5)
        restored = Transaction.from_dict({k: str(v) for k, v in original.to_dict().items()})
        self.assertEqual(restored.type, original.type)
        self.assertAlmostEqual(restored.amount, original.amount)
        self.assertEqual(restored.category, original.category)
        self.assertEqual(restored.date, original.date)
        self.assertEqual(restored.id, original.id)


class TestTransactionStr(unittest.TestCase):

    def test_returns_string(self):
        self.assertIsInstance(str(_t()), str)

    def test_contains_type(self):
        self.assertIn("expense", str(_t(type="expense")))

    def test_contains_category(self):
        self.assertIn("groceries", str(_t(category="groceries")))

    def test_contains_amount(self):
        self.assertIn("250.0", str(_t(amount=250.0)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
