"""
Tests for commands.py
Covers: all command verbs, argument parsing, error paths, color mode,
        output format, integration with store/budget/analyzer.
"""
import os
import sys
import unittest
from datetime import date
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import TempDirTest, capture, make_handler


TODAY = date.today().isoformat()


class TestHandleBasic(TempDirTest, unittest.TestCase):

    def test_empty_string_no_output(self):
        h = make_handler(self.tmp)
        self.assertEqual(capture(h, ""), "")

    def test_whitespace_only_no_output(self):
        h = make_handler(self.tmp)
        self.assertEqual(capture(h, "   "), "")

    def test_unknown_command_prints_unknown(self):
        h = make_handler(self.tmp)
        self.assertIn("Unknown", capture(h, "foobar"))

    def test_commands_are_case_sensitive(self):
        h = make_handler(self.tmp)
        for cmd in ["ADD", "List", "BUDGET", "Summary", "DELETE", "EXPORT"]:
            self.assertIn("Unknown", capture(h, f"{cmd} arg1 arg2"))

    def test_exception_from_store_is_caught(self):
        h = make_handler(self.tmp)
        h.store.add = MagicMock(side_effect=RuntimeError("disk full"))
        out = capture(h, "add income 100 salary Pay")
        self.assertIn("Error", out)


class TestHandleAdd(TempDirTest, unittest.TestCase):

    def test_add_income(self):
        h = make_handler(self.tmp)
        capture(h, "add income 500 salary Monthly pay")
        self.assertEqual(len(h.store.transactions), 1)
        self.assertEqual(h.store.transactions[0].type, "income")

    def test_add_expense(self):
        h = make_handler(self.tmp)
        capture(h, "add expense 100 food Lunch")
        self.assertEqual(h.store.transactions[0].type, "expense")

    def test_add_prints_positive_for_income(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income 500 salary Pay")
        self.assertIn("500.00", out)

    def test_add_prints_negative_for_expense(self):
        h = make_handler(self.tmp)
        out = capture(h, "add expense 100 food Lunch")
        self.assertIn("-100.00", out)

    def test_add_prints_category(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income 100 salary Pay")
        self.assertIn("salary", out)

    def test_add_prints_date(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income 100 salary Pay")
        self.assertIn(TODAY, out)

    def test_add_invalid_type_nothing_stored(self):
        h = make_handler(self.tmp)
        capture(h, "add transfer 100 misc")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_nonnumeric_amount_prints_error(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income abc salary Pay")
        self.assertTrue("Error" in out or "error" in out)

    def test_add_nonnumeric_amount_nothing_stored(self):
        h = make_handler(self.tmp)
        capture(h, "add income abc salary Pay")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_zero_amount_rejected(self):
        h = make_handler(self.tmp)
        capture(h, "add income 0 salary Pay")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_negative_amount_rejected(self):
        h = make_handler(self.tmp)
        capture(h, "add income -50 salary Pay")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_too_few_args_shows_usage(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income 100")
        self.assertIn("Usage", out)

    def test_add_too_few_args_nothing_stored(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_no_description_stores_empty_string(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary")
        self.assertEqual(h.store.transactions[0].description, "")

    def test_add_multiword_description_joined(self):
        h = make_handler(self.tmp)
        capture(h, "add expense 50 food Chicken rice and hummus")
        self.assertEqual(h.store.transactions[0].description, "Chicken rice and hummus")

    def test_add_with_date_flag(self):
        h = make_handler(self.tmp)
        capture(h, "add income 200 salary Pay --date 2024-03-15")
        self.assertEqual(h.store.transactions[0].date, "2024-03-15")

    def test_add_with_date_flag_description_before_flag(self):
        h = make_handler(self.tmp)
        capture(h, "add expense 50 food Chicken dinner --date 2024-05-01")
        self.assertEqual(h.store.transactions[0].description, "Chicken dinner")
        self.assertEqual(h.store.transactions[0].date, "2024-05-01")

    def test_add_date_flag_missing_value(self):
        h = make_handler(self.tmp)
        out = capture(h, "add income 200 salary Pay --date")
        self.assertTrue("Error" in out or len(h.store.transactions) == 0)

    def test_add_invalid_date_flag_value(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay --date 99-99-9999")
        self.assertEqual(len(h.store.transactions), 0)

    def test_add_large_amount(self):
        h = make_handler(self.tmp)
        capture(h, "add income 999999.99 salary Bonus")
        self.assertAlmostEqual(h.store.transactions[0].amount, 999999.99)

    def test_add_increments_ids_correctly(self):
        h = make_handler(self.tmp)
        for _ in range(5):
            capture(h, "add income 100 salary Pay")
        ids = [t.id for t in h.store.transactions]
        self.assertEqual(ids, [1, 2, 3, 4, 5])

    def test_add_float_amount_precision(self):
        h = make_handler(self.tmp)
        capture(h, "add expense 19.99 food Coffee")
        self.assertAlmostEqual(h.store.transactions[0].amount, 19.99)


class TestHandleList(TempDirTest, unittest.TestCase):

    def test_list_empty_no_output(self):
        h = make_handler(self.tmp)
        self.assertEqual(capture(h, "list"), "")

    def test_list_shows_transaction(self):
        h = make_handler(self.tmp)
        capture(h, "add income 500 salary Pay")
        out = capture(h, "list")
        self.assertIn("salary", out)
        self.assertIn("500.00", out)

    def test_list_expense_negative(self):
        h = make_handler(self.tmp)
        capture(h, "add expense 75 food Dinner")
        out = capture(h, "list")
        self.assertIn("-75.00", out)

    def test_list_category_filter(self):
        h = make_handler(self.tmp)
        capture(h, "add income 500 salary Pay")
        capture(h, "add expense 100 food Lunch")
        out = capture(h, "list food")
        self.assertIn("food", out)
        self.assertNotIn("salary", out)

    def test_list_filter_no_match_no_output(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay")
        out = capture(h, "list xyz")
        self.assertEqual(out, "")

    def test_list_shows_id(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay")
        out = capture(h, "list")
        self.assertIn("1", out)


class TestHandleBudget(TempDirTest, unittest.TestCase):

    def test_budget_set_stores_value(self):
        h = make_handler(self.tmp)
        capture(h, "budget food 300")
        self.assertEqual(h.budget_manager.get_budget("food"), 300.0)

    def test_budget_prints_confirmation(self):
        h = make_handler(self.tmp)
        out = capture(h, "budget food 300")
        self.assertIn("300.00", out)

    def test_budget_invalid_amount_message(self):
        h = make_handler(self.tmp)
        out = capture(h, "budget food abc")
        self.assertTrue("numeric" in out.lower() or "Budget" in out)

    def test_budget_zero_rejected(self):
        h = make_handler(self.tmp)
        capture(h, "budget food 0")
        self.assertIsNone(h.budget_manager.get_budget("food"))

    def test_budget_negative_rejected(self):
        h = make_handler(self.tmp)
        out = capture(h, "budget food -100")
        self.assertIn("positive", out.lower())

    def test_budget_too_few_args(self):
        h = make_handler(self.tmp)
        self.assertIn("Usage", capture(h, "budget food"))

    def test_budget_too_many_args(self):
        h = make_handler(self.tmp)
        self.assertIn("Usage", capture(h, "budget food 300 extra"))

    def test_budget_overwrites_existing(self):
        h = make_handler(self.tmp)
        capture(h, "budget food 300")
        capture(h, "budget food 500")
        self.assertEqual(h.budget_manager.get_budget("food"), 500.0)

    def test_budget_float_accepted(self):
        h = make_handler(self.tmp)
        capture(h, "budget food 99.50")
        self.assertAlmostEqual(h.budget_manager.get_budget("food"), 99.50)


class TestHandleSummary(TempDirTest, unittest.TestCase):

    def test_summary_empty_shows_zeros(self):
        h = make_handler(self.tmp)
        out = capture(h, "summary")
        self.assertIn("SUMMARY", out)
        self.assertIn("0.00", out)

    def test_summary_shows_income(self):
        h = make_handler(self.tmp)
        capture(h, f"add income 1000 salary Pay --date {TODAY}")
        out = capture(h, "summary")
        self.assertIn("1000.00", out)

    def test_summary_shows_expenses(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 200 food Lunch --date {TODAY}")
        out = capture(h, "summary")
        self.assertIn("200.00", out)

    def test_summary_shows_balance(self):
        h = make_handler(self.tmp)
        capture(h, f"add income 1000 salary Pay --date {TODAY}")
        capture(h, f"add expense 300 food Lunch --date {TODAY}")
        out = capture(h, "summary")
        self.assertIn("700.00", out)

    def test_summary_under_budget(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 100 food Lunch --date {TODAY}")
        capture(h, "budget food 500")
        self.assertIn("under budget", capture(h, "summary"))

    def test_summary_over_budget(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 600 food Lunch --date {TODAY}")
        capture(h, "budget food 500")
        self.assertIn("over budget", capture(h, "summary"))

    def test_summary_no_color_no_ansi_codes(self):
        h = make_handler(self.tmp, use_color=False)
        out = capture(h, "summary")
        self.assertNotIn("\033[", out)

    def test_summary_no_budget_shows_spent_only(self):
        h = make_handler(self.tmp)
        capture(h, f"add expense 50 food Lunch --date {TODAY}")
        out = capture(h, "summary")
        self.assertIn("food", out)
        self.assertNotIn("budget", out.lower())


class TestHandleDelete(TempDirTest, unittest.TestCase):

    def test_delete_valid(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay")
        out = capture(h, "delete 1")
        self.assertIn("Deleted", out)
        self.assertEqual(len(h.store.transactions), 0)

    def test_delete_nonexistent(self):
        h = make_handler(self.tmp)
        out = capture(h, "delete 999")
        self.assertIn("does not exist", out)

    def test_delete_invalid_id(self):
        h = make_handler(self.tmp)
        out = capture(h, "delete abc")
        self.assertIn("number", out.lower())

    def test_delete_float_id_rejected(self):
        h = make_handler(self.tmp)
        out = capture(h, "delete 1.5")
        self.assertIn("number", out.lower())

    def test_delete_missing_arg(self):
        h = make_handler(self.tmp)
        self.assertIn("Usage", capture(h, "delete"))

    def test_delete_too_many_args(self):
        h = make_handler(self.tmp)
        self.assertIn("Usage", capture(h, "delete 1 2"))

    def test_delete_zero_not_found(self):
        h = make_handler(self.tmp)
        self.assertIn("does not exist", capture(h, "delete 0"))

    def test_delete_removes_correct_item(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary A")
        capture(h, "add income 200 bonus B")
        capture(h, "delete 1")
        self.assertEqual(h.store.transactions[0].category, "bonus")


class TestHandleExport(TempDirTest, unittest.TestCase):

    def setUp(self):
        super().setUp()
        os.chdir(self.tmp)

    def test_export_all_prints_exported(self):
        h = make_handler(self.tmp)
        out = capture(h, "export")
        self.assertIn("Exported", out)

    def test_export_by_month_prints_filename(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay --date 2024-01-10")
        out = capture(h, "export 2024-01")
        self.assertIn("export_2024-01.csv", out)

    def test_export_creates_file(self):
        h = make_handler(self.tmp)
        capture(h, "add income 100 salary Pay")
        capture(h, "export")
        self.assertTrue(os.path.exists("export_all.csv"))


class TestHandleChart(TempDirTest, unittest.TestCase):

    def test_chart_no_month_calls_bar_chart_none(self):
        h = make_handler(self.tmp)
        capture(h, "chart")
        h.chart_generator.bar_chart.assert_called_once_with(None)

    def test_chart_with_month(self):
        h = make_handler(self.tmp)
        capture(h, "chart 2024-06")
        h.chart_generator.bar_chart.assert_called_once_with("2024-06")


if __name__ == "__main__":
    unittest.main(verbosity=2)
