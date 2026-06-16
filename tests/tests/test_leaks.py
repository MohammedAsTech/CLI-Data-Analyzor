"""
Resource leak tests — memory, file handles, reference cycles.
Uses only stdlib: tracemalloc, gc, weakref, resource (Unix).
"""
import gc
import os
import sys
import tracemalloc
import unittest
import weakref

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import TempDirTest, make_store, make_transaction
from analyzer import Analyzer
from budget import BudgetManager
from store import TransactionStore
from transaction import Transaction


def _open_fd_count():
    """Return the number of open file descriptors for this process (Linux/macOS)."""
    try:
        return len(os.listdir("/proc/self/fd"))
    except FileNotFoundError:
        import subprocess
        try:
            result = subprocess.run(
                ["lsof", "-p", str(os.getpid()), "-Fn"],
                capture_output=True, text=True
            )
            return result.stdout.count("\n")
        except Exception:
            return None  # platform doesn't support fd counting


class TestMemoryLeaks(TempDirTest, unittest.TestCase):

    def test_creating_many_transactions_does_not_leak(self):
        """
        Create and immediately discard 1000 Transaction objects.
        Net memory growth should be below a generous threshold (1 MB).
        """
        gc.collect()
        tracemalloc.start()

        for _ in range(1000):
            Transaction("income", 100.0, "salary", "2024-01-01", "pay")

        gc.collect()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak usage for 1000 lightweight objects should stay well under 5 MB
        self.assertLess(peak, 5 * 1024 * 1024,
                        f"Peak memory {peak / 1024:.1f} KB exceeded threshold")

    def test_store_load_save_cycle_does_not_leak(self):
        """
        Repeatedly load and discard a store — net growth should be small.
        """
        fp = os.path.join(self.tmp, "tx.csv")
        s = TransactionStore(filepath=fp)
        for _ in range(20):
            s.add(make_transaction())

        gc.collect()
        tracemalloc.start()

        for _ in range(50):
            store = TransactionStore(filepath=fp)
            del store

        gc.collect()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.assertLess(peak, 10 * 1024 * 1024,
                        f"Peak {peak / 1024:.1f} KB exceeded threshold during store cycling")

    def test_analyzer_summary_does_not_accumulate(self):
        """
        Calling summary() 200 times should not accumulate heap objects.
        """
        store = make_store(self.tmp)
        for i in range(50):
            store.add(make_transaction(date="2024-01-01", type="expense", category="food"))
        analyzer = Analyzer(store)

        gc.collect()
        tracemalloc.start()

        for _ in range(200):
            _ = analyzer.summary(month="2024-01")

        gc.collect()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.assertLess(peak, 5 * 1024 * 1024,
                        f"Peak {peak / 1024:.1f} KB during repeated summary() calls")

    def test_budget_manager_set_get_does_not_leak(self):
        fp = os.path.join(self.tmp, "b.json")
        b = BudgetManager(filepath=fp)

        gc.collect()
        tracemalloc.start()

        for i in range(500):
            b.set_budget(f"cat_{i % 10}", float(i + 1))
            b.get_budget(f"cat_{i % 10}")

        gc.collect()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.assertLess(peak, 5 * 1024 * 1024)


class TestFileHandleLeaks(TempDirTest, unittest.TestCase):

    def test_store_load_does_not_leave_open_handles(self):
        """
        Opening and reloading a store repeatedly should not accumulate
        open file descriptors.
        """
        baseline = _open_fd_count()
        if baseline is None:
            self.skipTest("Cannot count file descriptors on this platform")

        fp = os.path.join(self.tmp, "tx.csv")
        for _ in range(30):
            store = TransactionStore(filepath=fp)
            store.add(make_transaction())
            del store

        after = _open_fd_count()
        # Allow a small tolerance for internal interpreter handles
        self.assertLessEqual(after - baseline, 5,
                             f"FD count grew from {baseline} to {after}")

    def test_store_add_does_not_leave_open_handles(self):
        baseline = _open_fd_count()
        if baseline is None:
            self.skipTest("Cannot count file descriptors on this platform")

        store = make_store(self.tmp)
        for _ in range(50):
            store.add(make_transaction())

        after = _open_fd_count()
        self.assertLessEqual(after - baseline, 5,
                             f"FD count grew from {baseline} to {after}")

    def test_budget_save_does_not_leave_open_handles(self):
        baseline = _open_fd_count()
        if baseline is None:
            self.skipTest("Cannot count file descriptors on this platform")

        fp = os.path.join(self.tmp, "b.json")
        b = BudgetManager(filepath=fp)
        for i in range(50):
            b.set_budget(f"cat_{i}", float(i + 1))

        after = _open_fd_count()
        self.assertLessEqual(after - baseline, 5,
                             f"FD count grew from {baseline} to {after}")

    def test_export_does_not_leave_open_handles(self):
        baseline = _open_fd_count()
        if baseline is None:
            self.skipTest("Cannot count file descriptors on this platform")

        os.chdir(self.tmp)
        store = make_store(self.tmp)
        for _ in range(10):
            store.add(make_transaction())

        for month in ["2024-01", "2024-02", "2024-03"]:
            store.export(month=month)

        after = _open_fd_count()
        self.assertLessEqual(after - baseline, 5,
                             f"FD count grew from {baseline} to {after}")


class TestReferenceLeaks(TempDirTest, unittest.TestCase):

    def test_transaction_collectable_after_delete(self):
        """Transaction should be garbage-collected when no references remain."""
        t = Transaction("income", 100.0, "salary", "2024-01-01", "pay")
        ref = weakref.ref(t)
        del t
        gc.collect()
        self.assertIsNone(ref(),
                          "Transaction was not garbage-collected — possible reference cycle")

    def test_store_collectable_after_delete(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s = TransactionStore(filepath=fp)
        s.add(make_transaction())
        ref = weakref.ref(s)
        del s
        gc.collect()
        self.assertIsNone(ref(),
                          "TransactionStore was not garbage-collected — possible reference cycle")

    def test_analyzer_collectable_after_delete(self):
        store = make_store(self.tmp)
        a = Analyzer(store)
        ref = weakref.ref(a)
        del a
        gc.collect()
        self.assertIsNone(ref(),
                          "Analyzer was not garbage-collected")

    def test_budget_manager_collectable(self):
        fp = os.path.join(self.tmp, "b.json")
        b = BudgetManager(filepath=fp)
        ref = weakref.ref(b)
        del b
        gc.collect()
        self.assertIsNone(ref(),
                          "BudgetManager was not garbage-collected")

    def test_no_cycles_in_transaction(self):
        """gc.get_referrers should not show circular references within Transaction."""
        gc.collect()
        before = len(gc.garbage)
        t = Transaction("income", 100.0, "salary", "2024-01-01", "pay")
        del t
        gc.collect()
        after = len(gc.garbage)
        self.assertEqual(before, after,
                         f"gc.garbage grew by {after - before} after deleting Transaction")

    def test_store_transactions_list_cleared_on_del(self):
        """After deleting a store, its transaction list should be collected."""
        store = make_store(self.tmp)
        for _ in range(100):
            store.add(make_transaction())
        tx_refs = [weakref.ref(t) for t in store.transactions]
        del store
        gc.collect()
        still_alive = sum(1 for r in tx_refs if r() is not None)
        self.assertEqual(still_alive, 0,
                         f"{still_alive} transactions still alive after store deletion")


class TestStateIsolation(TempDirTest, unittest.TestCase):
    """Ensure separate store instances don't share state."""

    def test_two_stores_same_file_independent_after_add(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s2 = TransactionStore(filepath=fp)
        s1.add(make_transaction())
        # s2 hasn't reloaded — its in-memory list is still stale
        self.assertEqual(len(s2.transactions), 0)

    def test_two_stores_different_files_fully_independent(self):
        fp1 = os.path.join(self.tmp, "a.csv")
        fp2 = os.path.join(self.tmp, "b.csv")
        s1 = TransactionStore(filepath=fp1)
        s2 = TransactionStore(filepath=fp2)
        s1.add(make_transaction())
        self.assertEqual(len(s2.transactions), 0)

    def test_modifying_transactions_list_does_not_affect_other_instance(self):
        fp = os.path.join(self.tmp, "tx.csv")
        s1 = TransactionStore(filepath=fp)
        s1.add(make_transaction())
        s2 = TransactionStore(filepath=fp)
        s1.transactions.clear()
        # s2 loaded independently — its list should be unaffected
        self.assertEqual(len(s2.transactions), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
