# Test Results

**Run date:** 2026-06-16 12:39:25  
**Duration:** 11.12s  
**Overall:** ✅ ALL TESTS PASSED  

## Summary

| Status  | Count |
|---------|------:|
| ✅ Passed  | 303 |
| ❌ Failed  | 0 |
| 💥 Errors  | 0 |
| ⏭️ Skipped | 0 |
| **Total**  | **303** |
| **Pass rate** | **100.0%** |

## Results by Module

### ✅ `test_analyzer` — 35/35 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_category_names_are_lowercase` | `TestAnalyzerByCategory` | ✅ PASS | 12ms |
| 2 | `test_default_month_uses_today` | `TestAnalyzerByCategory` | ✅ PASS | 1ms |
| 3 | `test_empty_returns_empty_list` | `TestAnalyzerByCategory` | ✅ PASS | 0ms |
| 4 | `test_excludes_income` | `TestAnalyzerByCategory` | ✅ PASS | 1ms |
| 5 | `test_returns_list_of_2_tuples` | `TestAnalyzerByCategory` | ✅ PASS | 1ms |
| 6 | `test_sorted_descending_by_amount` | `TestAnalyzerByCategory` | ✅ PASS | 2ms |
| 7 | `test_top_category_first` | `TestAnalyzerByCategory` | ✅ PASS | 1ms |
| 8 | `test_income_expense_balance_consistent` | `TestAnalyzerFloatingPoint` | ✅ PASS | 1ms |
| 9 | `test_many_small_amounts_sum_accurately` | `TestAnalyzerFloatingPoint` | ✅ PASS | 58ms |
| 10 | `test_different_months_separate_entries` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 11 | `test_empty_store_returns_empty_list` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 0ms |
| 12 | `test_expense_only_month` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 13 | `test_income_only_month` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 14 | `test_invariant_totals_across_all_months` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 2ms |
| 15 | `test_month_key_format_yyyy_mm` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 16 | `test_multiple_months_sorted_chronologically` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 17 | `test_multiple_transactions_same_month_aggregated` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 18 | `test_returns_3_tuples` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 19 | `test_single_month_structure` | `TestAnalyzerMonthlyTotals` | ✅ PASS | 1ms |
| 20 | `test_balance_can_be_negative` | `TestAnalyzerSummaryBasic` | ✅ PASS | 0ms |
| 21 | `test_balance_can_be_zero` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 22 | `test_balance_income_minus_expenses` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 23 | `test_default_month_is_today` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 24 | `test_empty_store_all_zeros` | `TestAnalyzerSummaryBasic` | ✅ PASS | 0ms |
| 25 | `test_expense_only` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 26 | `test_future_month_returns_zeros` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 27 | `test_income_only` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 28 | `test_keys_always_present` | `TestAnalyzerSummaryBasic` | ✅ PASS | 0ms |
| 29 | `test_only_includes_current_month` | `TestAnalyzerSummaryBasic` | ✅ PASS | 1ms |
| 30 | `test_category_normalized_to_lowercase` | `TestAnalyzerSummaryCategories` | ✅ PASS | 1ms |
| 31 | `test_expenses_grouped_by_category` | `TestAnalyzerSummaryCategories` | ✅ PASS | 1ms |
| 32 | `test_expenses_total_equals_sum_of_categories` | `TestAnalyzerSummaryCategories` | ✅ PASS | 1ms |
| 33 | `test_income_not_in_expenses_by_category` | `TestAnalyzerSummaryCategories` | ✅ PASS | 0ms |
| 34 | `test_mixed_case_categories_merged` | `TestAnalyzerSummaryCategories` | ✅ PASS | 1ms |
| 35 | `test_multiple_categories_tracked_separately` | `TestAnalyzerSummaryCategories` | ✅ PASS | 1ms |

### ✅ `test_budget` — 29/29 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_corrupted_file_is_replaced` | `TestBudgetCorruption` | ✅ PASS | 0ms |
| 2 | `test_corrupted_json_does_not_crash` | `TestBudgetCorruption` | ✅ PASS | 0ms |
| 3 | `test_empty_file_handled` | `TestBudgetCorruption` | ✅ PASS | 0ms |
| 4 | `test_created_file_is_valid_json` | `TestBudgetInit` | ✅ PASS | 0ms |
| 5 | `test_creates_json_file` | `TestBudgetInit` | ✅ PASS | 0ms |
| 6 | `test_custom_filepath_stored` | `TestBudgetInit` | ✅ PASS | 0ms |
| 7 | `test_starts_empty` | `TestBudgetInit` | ✅ PASS | 0ms |
| 8 | `test_json_file_valid_after_set` | `TestBudgetPersistence` | ✅ PASS | 1ms |
| 9 | `test_multiple_categories_persist` | `TestBudgetPersistence` | ✅ PASS | 1ms |
| 10 | `test_multiple_instances_see_same_data` | `TestBudgetPersistence` | ✅ PASS | 0ms |
| 11 | `test_overwrite_persists` | `TestBudgetPersistence` | ✅ PASS | 1ms |
| 12 | `test_persists_after_set` | `TestBudgetPersistence` | ✅ PASS | 0ms |
| 13 | `test_get_normalizes_key_to_lowercase` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 14 | `test_get_unknown_returns_none` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 15 | `test_large_budget` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 16 | `test_multiple_categories_independent` | `TestBudgetSetGet` | ✅ PASS | 1ms |
| 17 | `test_overwrite_budget` | `TestBudgetSetGet` | ✅ PASS | 1ms |
| 18 | `test_raw_json_key_is_lowercase` | `TestBudgetSetGet` | ✅ PASS | 1ms |
| 19 | `test_set_and_get_basic` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 20 | `test_set_float_value` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 21 | `test_set_normalizes_key_to_lowercase` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 22 | `test_set_stores_as_float` | `TestBudgetSetGet` | ✅ PASS | 0ms |
| 23 | `test_empty_category_raises` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 24 | `test_error_message_mentions_category` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 25 | `test_error_message_mentions_positive` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 26 | `test_negative_limit_raises` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 27 | `test_rejected_budget_not_stored` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 28 | `test_small_positive_accepted` | `TestBudgetValidation` | ✅ PASS | 0ms |
| 29 | `test_zero_limit_raises` | `TestBudgetValidation` | ✅ PASS | 0ms |

### ✅ `test_commands` — 63/63 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_add_date_flag_missing_value` | `TestHandleAdd` | ✅ PASS | 1ms |
| 2 | `test_add_expense` | `TestHandleAdd` | ✅ PASS | 1ms |
| 3 | `test_add_float_amount_precision` | `TestHandleAdd` | ✅ PASS | 1ms |
| 4 | `test_add_income` | `TestHandleAdd` | ✅ PASS | 1ms |
| 5 | `test_add_increments_ids_correctly` | `TestHandleAdd` | ✅ PASS | 2ms |
| 6 | `test_add_invalid_date_flag_value` | `TestHandleAdd` | ✅ PASS | 1ms |
| 7 | `test_add_invalid_type_nothing_stored` | `TestHandleAdd` | ✅ PASS | 0ms |
| 8 | `test_add_large_amount` | `TestHandleAdd` | ✅ PASS | 1ms |
| 9 | `test_add_multiword_description_joined` | `TestHandleAdd` | ✅ PASS | 1ms |
| 10 | `test_add_negative_amount_rejected` | `TestHandleAdd` | ✅ PASS | 1ms |
| 11 | `test_add_no_description_stores_empty_string` | `TestHandleAdd` | ✅ PASS | 1ms |
| 12 | `test_add_nonnumeric_amount_nothing_stored` | `TestHandleAdd` | ✅ PASS | 0ms |
| 13 | `test_add_nonnumeric_amount_prints_error` | `TestHandleAdd` | ✅ PASS | 0ms |
| 14 | `test_add_prints_category` | `TestHandleAdd` | ✅ PASS | 1ms |
| 15 | `test_add_prints_date` | `TestHandleAdd` | ✅ PASS | 1ms |
| 16 | `test_add_prints_negative_for_expense` | `TestHandleAdd` | ✅ PASS | 1ms |
| 17 | `test_add_prints_positive_for_income` | `TestHandleAdd` | ✅ PASS | 2ms |
| 18 | `test_add_too_few_args_nothing_stored` | `TestHandleAdd` | ✅ PASS | 0ms |
| 19 | `test_add_too_few_args_shows_usage` | `TestHandleAdd` | ✅ PASS | 1ms |
| 20 | `test_add_with_date_flag` | `TestHandleAdd` | ✅ PASS | 1ms |
| 21 | `test_add_with_date_flag_description_before_flag` | `TestHandleAdd` | ✅ PASS | 1ms |
| 22 | `test_add_zero_amount_rejected` | `TestHandleAdd` | ✅ PASS | 0ms |
| 23 | `test_commands_are_case_sensitive` | `TestHandleBasic` | ✅ PASS | 0ms |
| 24 | `test_empty_string_no_output` | `TestHandleBasic` | ✅ PASS | 0ms |
| 25 | `test_exception_from_store_is_caught` | `TestHandleBasic` | ✅ PASS | 0ms |
| 26 | `test_unknown_command_prints_unknown` | `TestHandleBasic` | ✅ PASS | 0ms |
| 27 | `test_whitespace_only_no_output` | `TestHandleBasic` | ✅ PASS | 0ms |
| 28 | `test_budget_float_accepted` | `TestHandleBudget` | ✅ PASS | 1ms |
| 29 | `test_budget_invalid_amount_message` | `TestHandleBudget` | ✅ PASS | 0ms |
| 30 | `test_budget_negative_rejected` | `TestHandleBudget` | ✅ PASS | 1ms |
| 31 | `test_budget_overwrites_existing` | `TestHandleBudget` | ✅ PASS | 2ms |
| 32 | `test_budget_prints_confirmation` | `TestHandleBudget` | ✅ PASS | 1ms |
| 33 | `test_budget_set_stores_value` | `TestHandleBudget` | ✅ PASS | 1ms |
| 34 | `test_budget_too_few_args` | `TestHandleBudget` | ✅ PASS | 1ms |
| 35 | `test_budget_too_many_args` | `TestHandleBudget` | ✅ PASS | 1ms |
| 36 | `test_budget_zero_rejected` | `TestHandleBudget` | ✅ PASS | 1ms |
| 37 | `test_chart_no_month_calls_bar_chart_none` | `TestHandleChart` | ✅ PASS | 1ms |
| 38 | `test_chart_with_month` | `TestHandleChart` | ✅ PASS | 1ms |
| 39 | `test_delete_float_id_rejected` | `TestHandleDelete` | ✅ PASS | 1ms |
| 40 | `test_delete_invalid_id` | `TestHandleDelete` | ✅ PASS | 1ms |
| 41 | `test_delete_missing_arg` | `TestHandleDelete` | ✅ PASS | 1ms |
| 42 | `test_delete_nonexistent` | `TestHandleDelete` | ✅ PASS | 1ms |
| 43 | `test_delete_removes_correct_item` | `TestHandleDelete` | ✅ PASS | 2ms |
| 44 | `test_delete_too_many_args` | `TestHandleDelete` | ✅ PASS | 0ms |
| 45 | `test_delete_valid` | `TestHandleDelete` | ✅ PASS | 1ms |
| 46 | `test_delete_zero_not_found` | `TestHandleDelete` | ✅ PASS | 1ms |
| 47 | `test_export_all_prints_exported` | `TestHandleExport` | ✅ PASS | 1ms |
| 48 | `test_export_by_month_prints_filename` | `TestHandleExport` | ✅ PASS | 2ms |
| 49 | `test_export_creates_file` | `TestHandleExport` | ✅ PASS | 1ms |
| 50 | `test_list_category_filter` | `TestHandleList` | ✅ PASS | 2ms |
| 51 | `test_list_empty_no_output` | `TestHandleList` | ✅ PASS | 0ms |
| 52 | `test_list_expense_negative` | `TestHandleList` | ✅ PASS | 1ms |
| 53 | `test_list_filter_no_match_no_output` | `TestHandleList` | ✅ PASS | 1ms |
| 54 | `test_list_shows_id` | `TestHandleList` | ✅ PASS | 1ms |
| 55 | `test_list_shows_transaction` | `TestHandleList` | ✅ PASS | 1ms |
| 56 | `test_summary_empty_shows_zeros` | `TestHandleSummary` | ✅ PASS | 1ms |
| 57 | `test_summary_no_budget_shows_spent_only` | `TestHandleSummary` | ✅ PASS | 1ms |
| 58 | `test_summary_no_color_no_ansi_codes` | `TestHandleSummary` | ✅ PASS | 1ms |
| 59 | `test_summary_over_budget` | `TestHandleSummary` | ✅ PASS | 1ms |
| 60 | `test_summary_shows_balance` | `TestHandleSummary` | ✅ PASS | 1ms |
| 61 | `test_summary_shows_expenses` | `TestHandleSummary` | ✅ PASS | 1ms |
| 62 | `test_summary_shows_income` | `TestHandleSummary` | ✅ PASS | 1ms |
| 63 | `test_summary_under_budget` | `TestHandleSummary` | ✅ PASS | 1ms |

### ✅ `test_integration` — 19/19 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_add_delete_add_id_sequence` | `TestAddListDeleteWorkflow` | ✅ PASS | 1ms |
| 2 | `test_add_list_delete_cycle` | `TestAddListDeleteWorkflow` | ✅ PASS | 1ms |
| 3 | `test_multiple_adds_then_selective_delete` | `TestAddListDeleteWorkflow` | ✅ PASS | 1ms |
| 4 | `test_budget_overwrite_reflects_in_summary` | `TestBudgetSummaryWorkflow` | ✅ PASS | 1ms |
| 5 | `test_multiple_categories_budget_status` | `TestBudgetSummaryWorkflow` | ✅ PASS | 1ms |
| 6 | `test_set_budget_then_check_summary_over` | `TestBudgetSummaryWorkflow` | ✅ PASS | 1ms |
| 7 | `test_set_budget_then_check_summary_under` | `TestBudgetSummaryWorkflow` | ✅ PASS | 1ms |
| 8 | `test_export_then_reimport_preserves_data` | `TestCategoryNormalizationEndToEnd` | ✅ PASS | 1ms |
| 9 | `test_filter_and_summary_use_consistent_casing` | `TestCategoryNormalizationEndToEnd` | ✅ PASS | 1ms |
| 10 | `test_balance_always_income_minus_expenses` | `TestDataConsistencyInvariants` | ✅ PASS | 1ms |
| 11 | `test_by_category_amounts_sum_to_total_expenses` | `TestDataConsistencyInvariants` | ✅ PASS | 1ms |
| 12 | `test_monthly_totals_sum_matches_all_transactions` | `TestDataConsistencyInvariants` | ✅ PASS | 2ms |
| 13 | `test_store_count_consistent_after_add_delete_cycles` | `TestDataConsistencyInvariants` | ✅ PASS | 4ms |
| 14 | `test_store_ids_unique_after_sequential_adds` | `TestDataConsistencyInvariants` | ✅ PASS | 6ms |
| 15 | `test_summary_expenses_equals_sum_of_expense_transactions` | `TestDataConsistencyInvariants` | ✅ PASS | 1ms |
| 16 | `test_summary_income_equals_sum_of_income_transactions` | `TestDataConsistencyInvariants` | ✅ PASS | 1ms |
| 17 | `test_analyzer_works_on_reloaded_store` | `TestPersistenceAcrossRestarts` | ✅ PASS | 1ms |
| 18 | `test_budgets_survive_restart` | `TestPersistenceAcrossRestarts` | ✅ PASS | 0ms |
| 19 | `test_transactions_survive_restart` | `TestPersistenceAcrossRestarts` | ✅ PASS | 1ms |

### ✅ `test_leaks` — 17/17 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_budget_save_does_not_leave_open_handles` | `TestFileHandleLeaks` | ✅ PASS | 15ms |
| 2 | `test_export_does_not_leave_open_handles` | `TestFileHandleLeaks` | ✅ PASS | 4ms |
| 3 | `test_store_add_does_not_leave_open_handles` | `TestFileHandleLeaks` | ✅ PASS | 17ms |
| 4 | `test_store_load_does_not_leave_open_handles` | `TestFileHandleLeaks` | ✅ PASS | 8ms |
| 5 | `test_analyzer_summary_does_not_accumulate` | `TestMemoryLeaks` | ✅ PASS | 26ms |
| 6 | `test_budget_manager_set_get_does_not_leak` | `TestMemoryLeaks` | ✅ PASS | 173ms |
| 7 | `test_creating_many_transactions_does_not_leak` | `TestMemoryLeaks` | ✅ PASS | 20ms |
| 8 | `test_store_load_save_cycle_does_not_leak` | `TestMemoryLeaks` | ✅ PASS | 41ms |
| 9 | `test_analyzer_collectable_after_delete` | `TestReferenceLeaks` | ✅ PASS | 3ms |
| 10 | `test_budget_manager_collectable` | `TestReferenceLeaks` | ✅ PASS | 4ms |
| 11 | `test_no_cycles_in_transaction` | `TestReferenceLeaks` | ✅ PASS | 5ms |
| 12 | `test_store_collectable_after_delete` | `TestReferenceLeaks` | ✅ PASS | 5ms |
| 13 | `test_store_transactions_list_cleared_on_del` | `TestReferenceLeaks` | ✅ PASS | 48ms |
| 14 | `test_transaction_collectable_after_delete` | `TestReferenceLeaks` | ✅ PASS | 4ms |
| 15 | `test_modifying_transactions_list_does_not_affect_other_instance` | `TestStateIsolation` | ✅ PASS | 1ms |
| 16 | `test_two_stores_different_files_fully_independent` | `TestStateIsolation` | ✅ PASS | 1ms |
| 17 | `test_two_stores_same_file_independent_after_add` | `TestStateIsolation` | ✅ PASS | 1ms |

### ✅ `test_store` — 56/56 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_add_assigns_id_1_to_first` | `TestStoreAdd` | ✅ PASS | 1ms |
| 2 | `test_add_description_with_multiple_pipes` | `TestStoreAdd` | ✅ PASS | 0ms |
| 3 | `test_add_description_with_pipe_character` | `TestStoreAdd` | ✅ PASS | 1ms |
| 4 | `test_add_description_with_quotes` | `TestStoreAdd` | ✅ PASS | 0ms |
| 5 | `test_add_does_not_overwrite_preset_id` | `TestStoreAdd` | ✅ PASS | 0ms |
| 6 | `test_add_duplicate_preset_id_raises` | `TestStoreAdd` | ✅ PASS | 0ms |
| 7 | `test_add_expense_type_preserved` | `TestStoreAdd` | ✅ PASS | 0ms |
| 8 | `test_add_income_type_preserved` | `TestStoreAdd` | ✅ PASS | 1ms |
| 9 | `test_add_increases_count` | `TestStoreAdd` | ✅ PASS | 0ms |
| 10 | `test_add_increments_ids_sequentially` | `TestStoreAdd` | ✅ PASS | 1ms |
| 11 | `test_add_persists_immediately` | `TestStoreAdd` | ✅ PASS | 0ms |
| 12 | `test_add_preserves_all_fields` | `TestStoreAdd` | ✅ PASS | 0ms |
| 13 | `test_corrupted_file_is_overwritten` | `TestStoreCorruption` | ✅ PASS | 0ms |
| 14 | `test_garbage_file_starts_empty` | `TestStoreCorruption` | ✅ PASS | 0ms |
| 15 | `test_partial_corruption_is_handled` | `TestStoreCorruption` | ✅ PASS | 1ms |
| 16 | `test_delete_existing_returns_true` | `TestStoreDelete` | ✅ PASS | 1ms |
| 17 | `test_delete_from_empty_store` | `TestStoreDelete` | ✅ PASS | 0ms |
| 18 | `test_delete_is_idempotent_on_missing_id` | `TestStoreDelete` | ✅ PASS | 1ms |
| 19 | `test_delete_middle_item` | `TestStoreDelete` | ✅ PASS | 2ms |
| 20 | `test_delete_nonexistent_returns_false` | `TestStoreDelete` | ✅ PASS | 0ms |
| 21 | `test_delete_persists` | `TestStoreDelete` | ✅ PASS | 1ms |
| 22 | `test_delete_removes_correct_record` | `TestStoreDelete` | ✅ PASS | 1ms |
| 23 | `test_delete_removes_from_list` | `TestStoreDelete` | ✅ PASS | 1ms |
| 24 | `test_export_all_creates_file` | `TestStoreExport` | ✅ PASS | 1ms |
| 25 | `test_export_all_returns_correct_count` | `TestStoreExport` | ✅ PASS | 1ms |
| 26 | `test_export_all_returns_correct_filename` | `TestStoreExport` | ✅ PASS | 0ms |
| 27 | `test_export_by_month_filename` | `TestStoreExport` | ✅ PASS | 0ms |
| 28 | `test_export_by_month_filters_correctly` | `TestStoreExport` | ✅ PASS | 1ms |
| 29 | `test_export_empty_store` | `TestStoreExport` | ✅ PASS | 0ms |
| 30 | `test_export_file_has_correct_header` | `TestStoreExport` | ✅ PASS | 1ms |
| 31 | `test_filter_by_category` | `TestStoreFilter` | ✅ PASS | 1ms |
| 32 | `test_filter_by_month` | `TestStoreFilter` | ✅ PASS | 1ms |
| 33 | `test_filter_does_not_mutate_store` | `TestStoreFilter` | ✅ PASS | 1ms |
| 34 | `test_filter_month_and_category_combined` | `TestStoreFilter` | ✅ PASS | 2ms |
| 35 | `test_filter_no_args_returns_all` | `TestStoreFilter` | ✅ PASS | 1ms |
| 36 | `test_filter_no_match_returns_empty` | `TestStoreFilter` | ✅ PASS | 0ms |
| 37 | `test_creates_csv_file_on_first_run` | `TestStoreInit` | ✅ PASS | 0ms |
| 38 | `test_csv_file_has_header` | `TestStoreInit` | ✅ PASS | 0ms |
| 39 | `test_custom_filepath_stored` | `TestStoreInit` | ✅ PASS | 0ms |
| 40 | `test_new_store_is_empty` | `TestStoreInit` | ✅ PASS | 0ms |
| 41 | `test_category_filter` | `TestStoreListTransactions` | ✅ PASS | 1ms |
| 42 | `test_category_filter_case_insensitive` | `TestStoreListTransactions` | ✅ PASS | 1ms |
| 43 | `test_category_filter_no_match` | `TestStoreListTransactions` | ✅ PASS | 1ms |
| 44 | `test_empty_store_returns_empty_list` | `TestStoreListTransactions` | ✅ PASS | 0ms |
| 45 | `test_returns_all_transactions` | `TestStoreListTransactions` | ✅ PASS | 1ms |
| 46 | `test_sort_stability_same_date` | `TestStoreListTransactions` | ✅ PASS | 1ms |
| 47 | `test_sorted_descending_by_date` | `TestStoreListTransactions` | ✅ PASS | 2ms |
| 48 | `test_after_all_deleted_resets_to_1` | `TestStoreNextId` | ✅ PASS | 1ms |
| 49 | `test_after_delete_uses_remaining_max` | `TestStoreNextId` | ✅ PASS | 1ms |
| 50 | `test_after_one_add` | `TestStoreNextId` | ✅ PASS | 0ms |
| 51 | `test_empty_store_returns_1` | `TestStoreNextId` | ✅ PASS | 0ms |
| 52 | `test_uses_max_not_count` | `TestStoreNextId` | ✅ PASS | 1ms |
| 53 | `test_amount_precision_survives_reload` | `TestStorePersistenceRoundtrip` | ✅ PASS | 1ms |
| 54 | `test_full_roundtrip_all_fields` | `TestStorePersistenceRoundtrip` | ✅ PASS | 0ms |
| 55 | `test_ids_survive_reload` | `TestStorePersistenceRoundtrip` | ✅ PASS | 1ms |
| 56 | `test_multiple_transactions_roundtrip` | `TestStorePersistenceRoundtrip` | ✅ PASS | 4ms |

### ✅ `test_stress` — 20/20 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_description_with_all_special_chars` | `TestEdgeCaseInputs` | ✅ PASS | 0ms |
| 2 | `test_description_with_pipe_character_roundtrip` | `TestEdgeCaseInputs` | ✅ PASS | 0ms |
| 3 | `test_maximum_practical_amount_roundtrip` | `TestEdgeCaseInputs` | ✅ PASS | 0ms |
| 4 | `test_minimum_valid_amount_precision` | `TestEdgeCaseInputs` | ✅ PASS | 0ms |
| 5 | `test_transaction_with_empty_description_roundtrip` | `TestEdgeCaseInputs` | ✅ PASS | 0ms |
| 6 | `test_unicode_in_all_fields_roundtrip` | `TestEdgeCaseInputs` | ✅ PASS | 1ms |
| 7 | `test_very_long_description_stored_and_retrieved` | `TestEdgeCaseInputs` | ✅ PASS | 1ms |
| 8 | `test_add_1000_transactions` | `TestLargeDataset` | ✅ PASS | 1380ms |
| 9 | `test_by_category_100_categories` | `TestLargeDataset` | ✅ PASS | 35ms |
| 10 | `test_filter_over_large_dataset_accuracy` | `TestLargeDataset` | ✅ PASS | 1184ms |
| 11 | `test_list_transactions_sorted_correctly_at_scale` | `TestLargeDataset` | ✅ PASS | 106ms |
| 12 | `test_monthly_totals_200_months_no_crash` | `TestLargeDataset` | ✅ PASS | 100ms |
| 13 | `test_reload_1000_transactions` | `TestLargeDataset` | ✅ PASS | 1488ms |
| 14 | `test_summary_over_large_dataset` | `TestLargeDataset` | ✅ PASS | 1487ms |
| 15 | `test_1000_adds_under_threshold` | `TestPerformanceBenchmarks` | ✅ PASS | 1502ms |
| 16 | `test_filter_1000_transactions_under_threshold` | `TestPerformanceBenchmarks` | ✅ PASS | 1392ms |
| 17 | `test_summary_1000_transactions_under_threshold` | `TestPerformanceBenchmarks` | ✅ PASS | 1439ms |
| 18 | `test_interleaved_add_delete_consistent_ids` | `TestRapidCycles` | ✅ PASS | 53ms |
| 19 | `test_rapid_add_200_then_delete_all` | `TestRapidCycles` | ✅ PASS | 211ms |
| 20 | `test_rapid_add_delete_200_cycles` | `TestRapidCycles` | ✅ PASS | 128ms |

### ✅ `test_transaction` — 64/64 passed

| # | Test | Class | Status | Time |
|---|------|-------|--------|-----:|
| 1 | `test_empty_description_accepted` | `TestTransactionDescription` | ✅ PASS | 0ms |
| 2 | `test_none_description_accepted` | `TestTransactionDescription` | ✅ PASS | 0ms |
| 3 | `test_normal_description` | `TestTransactionDescription` | ✅ PASS | 0ms |
| 4 | `test_unicode_description` | `TestTransactionDescription` | ✅ PASS | 0ms |
| 5 | `test_very_long_description` | `TestTransactionDescription` | ✅ PASS | 0ms |
| 6 | `test_basic_roundtrip` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 7 | `test_expense_roundtrip` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 8 | `test_full_roundtrip_via_dicts` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 9 | `test_invalid_type_raises_value_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 10 | `test_key_error_has_helpful_message` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 11 | `test_missing_amount_raises_key_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 12 | `test_missing_category_raises_key_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 13 | `test_missing_date_raises_key_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 14 | `test_missing_id_raises_key_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 15 | `test_missing_type_raises_key_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 16 | `test_negative_amount_raises_value_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 17 | `test_nonnumeric_amount_raises_value_error` | `TestTransactionFromDict` | ✅ PASS | 0ms |
| 18 | `test_default_id_is_none` | `TestTransactionId` | ✅ PASS | 0ms |
| 19 | `test_explicit_id_stored` | `TestTransactionId` | ✅ PASS | 0ms |
| 20 | `test_id_large` | `TestTransactionId` | ✅ PASS | 0ms |
| 21 | `test_id_zero` | `TestTransactionId` | ✅ PASS | 0ms |
| 22 | `test_contains_amount` | `TestTransactionStr` | ✅ PASS | 0ms |
| 23 | `test_contains_category` | `TestTransactionStr` | ✅ PASS | 0ms |
| 24 | `test_contains_type` | `TestTransactionStr` | ✅ PASS | 0ms |
| 25 | `test_returns_string` | `TestTransactionStr` | ✅ PASS | 0ms |
| 26 | `test_all_keys_present` | `TestTransactionToDict` | ✅ PASS | 0ms |
| 27 | `test_mutating_dict_does_not_affect_transaction` | `TestTransactionToDict` | ✅ PASS | 0ms |
| 28 | `test_returns_independent_copies` | `TestTransactionToDict` | ✅ PASS | 0ms |
| 29 | `test_values_match_attributes` | `TestTransactionToDict` | ✅ PASS | 0ms |
| 30 | `test_error_message_mentions_positive` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 31 | `test_float_zero_rejected` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 32 | `test_large_amount` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 33 | `test_large_negative_rejected` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 34 | `test_minimum_positive` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 35 | `test_negative_rejected` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 36 | `test_positive_float` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 37 | `test_positive_integer` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 38 | `test_zero_rejected` | `TestTransactionValidAmount` | ✅ PASS | 0ms |
| 39 | `test_category_with_spaces` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 40 | `test_empty_string_rejected` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 41 | `test_error_message_mentions_category` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 42 | `test_none_category_rejected` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 43 | `test_numeric_string_category` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 44 | `test_simple_string` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 45 | `test_unicode_category` | `TestTransactionValidCategory` | ✅ PASS | 0ms |
| 46 | `test_day_32_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 47 | `test_far_future` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 48 | `test_invalid_leap_day_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 49 | `test_leap_day` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 50 | `test_month_13_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 51 | `test_month_only_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 52 | `test_reversed_format_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 53 | `test_slash_separator_rejected` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 54 | `test_standard_date` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 55 | `test_year_2000` | `TestTransactionValidDate` | ✅ PASS | 0ms |
| 56 | `test_empty_type_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 57 | `test_error_message_mentions_type` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 58 | `test_expense_accepted` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 59 | `test_income_accepted` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 60 | `test_none_type_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 61 | `test_transfer_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 62 | `test_uppercase_expense_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 63 | `test_uppercase_income_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |
| 64 | `test_whitespace_type_rejected` | `TestTransactionValidType` | ✅ PASS | 0ms |

## Failures & Errors

_No failures or errors — all tests passed._

## Top 10 Slowest Tests

| Rank | Test | Time |
|-----:|------|-----:|
| 1 | `TestPerformanceBenchmarks.test_1000_adds_under_threshold` | 1502ms |
| 2 | `TestLargeDataset.test_reload_1000_transactions` | 1488ms |
| 3 | `TestLargeDataset.test_summary_over_large_dataset` | 1487ms |
| 4 | `TestPerformanceBenchmarks.test_summary_1000_transactions_under_threshold` | 1439ms |
| 5 | `TestPerformanceBenchmarks.test_filter_1000_transactions_under_threshold` | 1392ms |
| 6 | `TestLargeDataset.test_add_1000_transactions` | 1380ms |
| 7 | `TestLargeDataset.test_filter_over_large_dataset_accuracy` | 1184ms |
| 8 | `TestRapidCycles.test_rapid_add_200_then_delete_all` | 211ms |
| 9 | `TestMemoryLeaks.test_budget_manager_set_get_does_not_leak` | 173ms |
| 10 | `TestRapidCycles.test_rapid_add_delete_200_cycles` | 128ms |
