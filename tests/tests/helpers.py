"""Shared test utilities used across all test modules."""
import os
import sys
import tempfile
import shutil
from io import StringIO
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import Analyzer
from budget import BudgetManager
from commands import CommandHandler
from store import TransactionStore
from transaction import Transaction


def make_transaction(
    type="income",
    amount=100.0,
    category="salary",
    date="2024-01-15",
    description="Test transaction",
    id=None,
):
    return Transaction(type, amount, category, date, description, id)


def make_store(dirpath):
    return TransactionStore(filepath=os.path.join(dirpath, "tx.csv"))


def make_budget(dirpath):
    return BudgetManager(filepath=os.path.join(dirpath, "budgets.json"))


def make_analyzer(store):
    return Analyzer(store)


def make_handler(dirpath, use_color=False):
    store = make_store(dirpath)
    analyzer = make_analyzer(store)
    budget = make_budget(dirpath)
    chart = MagicMock()
    return CommandHandler(store, analyzer, budget, chart, use_color=use_color)


def capture(handler, command):
    """Run a command and return captured stdout as a string."""
    buf = StringIO()
    with patch("sys.stdout", buf):
        handler.handle(command)
    return buf.getvalue()


class TempDirTest:
    """Mixin providing a fresh temp directory per test with automatic cleanup."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._orig_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self._orig_dir)
        shutil.rmtree(self.tmp, ignore_errors=True)
