"""
Test runner — discovers and runs all tests in the tests/ folder,
prints a live summary to the terminal, and writes TEST_RESULTS.md.

Usage:
    python tests/run_tests.py
"""
import os
import sys
import unittest
import io
import time
from datetime import datetime

# Make sure the project root is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, TESTS_DIR)


# ── Custom result collector ───────────────────────────────────────────────────

class DetailedResult(unittest.TestResult):
    """Collects per-test timings and full failure tracebacks."""

    def __init__(self):
        super().__init__()
        self.results = []          # list of (module, class, method, status, duration, detail)
        self._start_times = {}

    def startTest(self, test):
        super().startTest(test)
        self._start_times[test] = time.monotonic()

    def _record(self, test, status, detail=""):
        elapsed = time.monotonic() - self._start_times.get(test, time.monotonic())
        parts = test.id().rsplit(".", 2)
        module = parts[0] if len(parts) > 2 else ""
        cls    = parts[-2] if len(parts) >= 2 else ""
        method = parts[-1]
        self.results.append((module, cls, method, status, elapsed, detail))

    def addSuccess(self, test):
        self._record(test, "PASS")

    def addFailure(self, test, err):
        import traceback
        self._record(test, "FAIL", traceback.format_exception(*err)[-1].strip())

    def addError(self, test, err):
        import traceback
        self._record(test, "ERROR", traceback.format_exception(*err)[-1].strip())

    def addSkip(self, test, reason):
        self._record(test, "SKIP", reason)

    def addExpectedFailure(self, test, err):
        self._record(test, "XFAIL")

    def addUnexpectedSuccess(self, test):
        self._record(test, "XPASS")


# ── Discovery and run ─────────────────────────────────────────────────────────

def run_all():
    loader = unittest.TestLoader()
    suite  = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")

    result = DetailedResult()
    # Silence stdout from the tests themselves (warnings, prints)
    # but still show test progress via stderr
    total_start = time.monotonic()
    stderr_backup = sys.stderr

    # Live progress counter
    original_run = result.startTest
    counter = [0]
    total = suite.countTestCases()

    def progress_start(test):
        original_run(test)
        counter[0] += 1
        stderr_backup.write(f"\r  Running test {counter[0]}/{total} ...  ")
        stderr_backup.flush()

    result.startTest = progress_start

    suite.run(result)
    total_elapsed = time.monotonic() - total_start
    sys.stderr.write("\r" + " " * 50 + "\r")   # clear progress line

    return result, total_elapsed


# ── Report generation ─────────────────────────────────────────────────────────

def _status_icon(status):
    return {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭️",
            "XFAIL": "🔶", "XPASS": "⭐"}.get(status, "?")


def build_report(result, elapsed):
    rows = result.results
    passed  = sum(1 for r in rows if r[3] == "PASS")
    failed  = sum(1 for r in rows if r[3] == "FAIL")
    errors  = sum(1 for r in rows if r[3] == "ERROR")
    skipped = sum(1 for r in rows if r[3] == "SKIP")
    total   = len(rows)
    ok      = failed == 0 and errors == 0

    lines = []
    a = lines.append

    a("# Test Results")
    a("")
    a(f"**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    a(f"**Duration:** {elapsed:.2f}s  ")
    a(f"**Overall:** {'✅ ALL TESTS PASSED' if ok else '❌ SOME TESTS FAILED'}  ")
    a("")

    # ── Summary table ──
    a("## Summary")
    a("")
    a("| Status  | Count |")
    a("|---------|------:|")
    a(f"| ✅ Passed  | {passed} |")
    a(f"| ❌ Failed  | {failed} |")
    a(f"| 💥 Errors  | {errors} |")
    a(f"| ⏭️ Skipped | {skipped} |")
    a(f"| **Total**  | **{total}** |")
    a(f"| **Pass rate** | **{100 * passed / total:.1f}%** |" if total else "")
    a("")

    # ── Per-module breakdown ──
    a("## Results by Module")
    a("")

    # Group by module
    modules = {}
    for module, cls, method, status, dur, detail in rows:
        short_module = module.split(".")[-1] if module else "unknown"
        modules.setdefault(short_module, []).append((cls, method, status, dur, detail))

    for mod_name in sorted(modules):
        mod_rows = modules[mod_name]
        mod_pass = sum(1 for r in mod_rows if r[2] == "PASS")
        mod_total = len(mod_rows)
        icon = "✅" if mod_pass == mod_total else "❌"
        a(f"### {icon} `{mod_name}` — {mod_pass}/{mod_total} passed")
        a("")
        a("| # | Test | Class | Status | Time |")
        a("|---|------|-------|--------|-----:|")
        for i, (cls, method, status, dur, _) in enumerate(mod_rows, 1):
            s_icon = _status_icon(status)
            a(f"| {i} | `{method}` | `{cls}` | {s_icon} {status} | {dur*1000:.0f}ms |")
        a("")

    # ── Failures detail ──
    failures = [(m, c, mth, d) for m, c, mth, s, _, d in rows if s in ("FAIL", "ERROR")]
    if failures:
        a("## Failures & Errors")
        a("")
        for mod, cls, method, detail in failures:
            a(f"### ❌ `{cls}.{method}`")
            a(f"**Module:** `{mod}`  ")
            a("```")
            a(detail)
            a("```")
            a("")
    else:
        a("## Failures & Errors")
        a("")
        a("_No failures or errors — all tests passed._")
        a("")

    # ── Slowest tests ──
    slowest = sorted(rows, key=lambda r: r[4], reverse=True)[:10]
    a("## Top 10 Slowest Tests")
    a("")
    a("| Rank | Test | Time |")
    a("|-----:|------|-----:|")
    for rank, (mod, cls, method, status, dur, _) in enumerate(slowest, 1):
        a(f"| {rank} | `{cls}.{method}` | {dur*1000:.0f}ms |")
    a("")

    return "\n".join(lines)


# ── Terminal summary ──────────────────────────────────────────────────────────

def print_terminal_summary(result, elapsed):
    rows = result.results
    passed  = sum(1 for r in rows if r[3] == "PASS")
    failed  = sum(1 for r in rows if r[3] == "FAIL")
    errors  = sum(1 for r in rows if r[3] == "ERROR")
    skipped = sum(1 for r in rows if r[3] == "SKIP")
    total   = len(rows)
    ok      = failed == 0 and errors == 0

    sep = "=" * 60
    print(sep)
    print("  TEST RESULTS")
    print(sep)
    print(f"  Total   : {total}")
    print(f"  Passed  : {passed}")
    print(f"  Failed  : {failed}")
    print(f"  Errors  : {errors}")
    print(f"  Skipped : {skipped}")
    print(f"  Time    : {elapsed:.2f}s")
    print(sep)

    if ok:
        print("  ✅  ALL TESTS PASSED")
    else:
        print("  ❌  SOME TESTS FAILED\n")
        for mod, cls, method, status, _, detail in rows:
            if status in ("FAIL", "ERROR"):
                print(f"  [{status}] {cls}.{method}")
                if detail:
                    for line in detail.splitlines():
                        print(f"         {line}")
                print()

    print(sep)
    out_path = os.path.join(TESTS_DIR, "TEST_RESULTS.md")
    print(f"  Report  : {out_path}")
    print(sep)
    return ok


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("\nDiscovering tests in tests/ ...")
    result, elapsed = run_all()

    report_md = build_report(result, elapsed)
    out_path   = os.path.join(TESTS_DIR, "TEST_RESULTS.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    ok = print_terminal_summary(result, elapsed)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
