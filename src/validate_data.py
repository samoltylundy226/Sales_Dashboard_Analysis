"""
Data Validation and Quality Assurance
======================================

Project: Sales Dashboard Analysis
Module: src.validate_data
Author: Team Member 1 (Data Engineering) & Team Reviewers

Purpose:
--------
This module performs automated data quality checks, schema verification, and
integrity constraints on both raw and processed datasets before feeding them
into Power BI or SQL analytics pipelines.

Planned Validation Checks:
--------------------------
1. Schema & Column Presence: Verify required business columns exist.
2. Uniqueness: Check for primary key violations (e.g., unique order IDs or line items).
3. Null Constraints: Ensure mandatory columns (dates, sales amounts, IDs) contain no nulls.
4. Value Range & Bounds: Ensure prices, quantities, and discounts fall within realistic boundaries.
5. Temporal Validity: Ensure transaction dates are formatted correctly and within the expected project timeframe.
6. Data Type Conformance: Verify numerical and date fields are stored in correct dtypes.

Note:
-----
Thresholds, expected columns, and business rules will be configured after dataset selection.
"""

from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def check_required_columns(df: pd.DataFrame, expected_columns: List[str]) -> Dict[str, Any]:
    """
    Verify that all expected columns exist in the DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to validate.
    expected_columns : List[str]
        List of required column headers.

    Returns:
    --------
    Dict[str, Any]
        Validation outcome summary.
    """
    missing = [col for col in expected_columns if col not in df.columns]
    passed = len(missing) == 0
    return {
        "check": "required_columns",
        "passed": passed,
        "missing_columns": missing,
        "message": "All required columns are present." if passed else f"Missing columns: {missing}"
    }


def check_missing_rates(df: pd.DataFrame, threshold: float = 0.05) -> Dict[str, Any]:
    """
    Check if any column exceeds an acceptable missingness threshold.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to validate.
    threshold : float
        Maximum allowable fraction of null values (default: 5%).

    Returns:
    --------
    Dict[str, Any]
        Columns exceeding the threshold.
    """
    null_ratios = df.isnull().mean()
    failing_cols = null_ratios[null_ratios > threshold].to_dict()
    passed = len(failing_cols) == 0
    return {
        "check": "missing_rates",
        "passed": passed,
        "failing_columns": failing_cols,
        "message": "Missing rates are within acceptable limits." if passed else f"Columns exceeding {threshold*100}% nulls: {failing_cols}"
    }


def check_numeric_ranges(df: pd.DataFrame, range_rules: Dict[str, tuple]) -> Dict[str, Any]:
    """
    Validate that numerical columns fall within defined lower and upper bounds.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to validate.
    range_rules : Dict[str, tuple]
        Mapping of column name to (min_val, max_val).

    Returns:
    --------
    Dict[str, Any]
        Range validation report.
    """
    violations = {}
    for col, (min_val, max_val) in range_rules.items():
        if col in df.columns:
            out_of_bounds = df[(df[col] < min_val) | (df[col] > max_val)]
            if len(out_of_bounds) > 0:
                violations[col] = len(out_of_bounds)

    passed = len(violations) == 0
    return {
        "check": "numeric_ranges",
        "passed": passed,
        "violations": violations,
        "message": "All numeric values within valid bounds." if passed else f"Out of bounds records: {violations}"
    }


def run_validations(target_file: Path) -> bool:
    """
    Execute all validation rules against a target processed file.
    """
    print("=" * 60)
    print("Starting Data Quality Validation...")
    print("=" * 60)

    if not target_file.exists():
        print(f"[WARN] Target validation file does not exist: {target_file}")
        print("[ACTION] Run src/clean_data.py first to generate the processed dataset.")
        return False

    df = pd.read_csv(target_file)
    print(f"[INFO] Loaded dataset for validation: {target_file.name} ({len(df)} rows)")

    # Example placeholder checks (to be finalized with team)
    sample_expected_cols = list(df.columns)
    results = [
        check_required_columns(df, sample_expected_cols),
        check_missing_rates(df, threshold=0.05)
    ]

    all_passed = True
    for res in results:
        status_tag = "[PASS]" if res["passed"] else "[FAIL]"
        print(f"{status_tag} {res['check']}: {res['message']}")
        if not res["passed"]:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("[SUCCESS] All data validation checks passed.")
    else:
        print("[WARNING] One or more validation checks failed. Please inspect logs.")
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    processed_sample = PROCESSED_DATA_DIR / "sales_cleaned.csv"
    run_validations(processed_sample)
