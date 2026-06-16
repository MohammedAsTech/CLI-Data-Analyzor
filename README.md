# CLI Personal Finance Tracker

A command-line personal finance application built in Python. Track income and expenses, manage category budgets, analyze spending trends, and generate visualizations — all from a single interactive shell session with zero external runtime dependencies.

---

## Why This Project

This project demonstrates end-to-end ownership of a production-grade Python codebase: clean architecture, robust file I/O with edge-case handling, a 303-test suite covering unit, integration, memory, and stress scenarios, and documented bug discovery and remediation.

---

## Features

- **Transaction management** — add, list, delete income and expense records
- **Persistent storage** — pipe-delimited CSV with full quoting to handle special characters safely
- **Budget tracking** — per-category spending limits with over/under-budget alerts (ANSI color coded)
- **Financial analytics** — monthly summaries, category breakdowns, balance calculation
- **Spending charts** — horizontal bar charts exported as PNG via matplotlib
- **Data export** — filtered CSV export by month or full history
- **Corruption recovery** — automatic detection and recovery from malformed CSV/JSON files

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| Storage | CSV (`\|` delimiter, RFC-compliant quoting) · JSON |
| Charts | matplotlib |
| Testing | unittest (stdlib) · tracemalloc · weakref · gc |
| CLI | stdin/stdout loop, ANSI color output |

No third-party runtime dependencies beyond matplotlib.

---

## Project Structure

```
.
├── main.py              # Entry point — REPL loop
├── transaction.py       # Transaction model with validation
├── store.py             # CSV persistence layer
├── budget.py            # JSON budget manager
├── analyzer.py          # Financial analytics engine
├── commands.py          # Command handler (dispatch + formatting)
├── chart.py             # matplotlib chart generator
└── tests/
    ├── run_tests.py          # Custom test runner → TEST_RESULTS.md
    ├── helpers.py            # Shared test utilities and fixtures
    ├── test_transaction.py   # 54 tests
    ├── test_store.py         # 64 tests
    ├── test_budget.py        # 38 tests
    ├── test_analyzer.py      # 56 tests
    ├── test_commands.py      # 54 tests
    ├── test_integration.py   # 22 tests
    ├── test_leaks.py         # 27 tests
    ├── test_stress.py        # 28 tests
    ├── TEST_RESULTS.md       # Auto-generated test report
    └── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/<your-username>/CLIDataAnalyzerProject.git
cd CLIDataAnalyzerProject
pip install matplotlib
```

No virtual environment required — all other dependencies are Python stdlib.

---

## Usage

Start the interactive shell:

```bash
python main.py
```

### Commands

```
add <income|expense> <amount> <category> <description> [--date YYYY-MM-DD]
list [category]
budget <category> <limit>
summary
chart [YYYY-MM]
delete <id>
export [YYYY-MM]
exit
```

### Example Session

```
> add expense 45.50 food groceries --date 2026-06-01
Added: -45.50 NIS | food | 2026-06-01

> add income 3000 salary monthly-pay --date 2026-06-01
Added: 3000.00 NIS | salary | 2026-06-01

> budget food 500
Budget set: food -> 500.00 NIS

> summary

===== SUMMARY =====
Income   : 3000.00 NIS
Expenses : 45.50 NIS
Balance  : 2954.50 NIS

food: 45.50 / 500.00 NIS (454.50 remaining) [under budget]

> chart 2026-06
Chart saved to spending_2026-06.png

> export 2026-06
Exported 2 transactions to export_2026-06.csv

> exit
```

---

## Testing

Run the full test suite with a single command:

```bash
python tests/run_tests.py
```

This runs all 303 tests and writes a detailed report to `tests/TEST_RESULTS.md` including per-module results, timing, and failure traces.

### Test Coverage

| Module | Tests | What's Covered |
|---|---|---|
| `test_transaction.py` | 54 | Validation, boundary values, serialization, all missing-key combinations |
| `test_store.py` | 64 | CRUD, CSV quoting regression, corruption recovery, persistence roundtrip |
| `test_budget.py` | 38 | Set/get, case normalization, negative/zero rejection, JSON corruption recovery |
| `test_analyzer.py` | 56 | Summary filtering, category normalization, monthly totals, floating-point accuracy |
| `test_commands.py` | 54 | All commands, argument validation, color mode, error paths |
| `test_integration.py` | 22 | Cross-module workflows, persistence across restarts, data-consistency invariants |
| `test_leaks.py` | 27 | Memory (tracemalloc), file descriptor leaks (/proc/self/fd), reference cycles (weakref + gc) |
| `test_stress.py` | 28 | 1 000-record datasets, rapid add/delete cycles, unicode, special characters, performance benchmarks |
| **Total** | **303** | |

---

## Bugs Found and Fixed

A full audit of the codebase identified and fixed **7 bugs**:

| # | File | Bug | Fix |
|---|---|---|---|
| 1 | `analyzer.py` | Category keys were case-sensitive — `"Food"` and `"food"` created separate buckets | Normalize to `.lower()` before aggregation |
| 2 | `store.py` | No quoting on CSV writer/reader — pipe characters in descriptions corrupted rows | Added `quotechar='"'` and `quoting=csv.QUOTE_ALL` to both reader and writer |
| 3 | `store.py` | Corruption detected but file not overwritten — bad data reloaded on next start | Call `self.save()` after clearing transactions |
| 4 | `store.py` | Preset IDs could be silently duplicated on `add()` | Check for duplicate ID and raise `ValueError` |
| 5 | `budget.py` | Malformed `budgets.json` caused unhandled `JSONDecodeError` crash | Wrap `json.load()` in try/except; reset and save clean file |
| 6 | `budget.py` | Empty category string and non-positive limits accepted silently | Explicit validation with descriptive `ValueError` |
| 7 | `transaction.py` | Missing dict keys in `from_dict()` raised bare `KeyError` with no context | Wrap in try/except and re-raise with field name in message |

Each bug has a corresponding regression test that would have caught it before shipping.

---

## Skills Demonstrated

- **Python OOP** — separation of concerns across model / persistence / business logic / presentation layers
- **File I/O robustness** — RFC-compliant CSV handling, atomic-style save, corruption detection and recovery
- **Test engineering** — 303 tests across 8 modules; custom `unittest.TestResult` subclass for markdown report generation
- **Memory and resource safety** — `tracemalloc` memory budgets, file descriptor leak assertions, garbage-collection verification with `weakref`
- **Performance validation** — stress tests asserting sub-2-second load/filter/summary over 1 000-record datasets
- **Bug discovery methodology** — static analysis + regression tests + integration invariants

---
 
