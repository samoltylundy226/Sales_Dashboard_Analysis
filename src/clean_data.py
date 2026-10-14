"""
Data Cleaning and Preprocessing Pipeline
=========================================

Project: Sales Dashboard Analysis
Module: src.clean_data
Author: Team Member 1 (Data Engineering)

Purpose:
--------
This script provides the foundation for our automated data ingestion, cleaning,
and preprocessing pipeline. It prepares raw sales data for downstream exploratory
analysis, SQL modeling, and Power BI dashboard consumption.

Planned Responsibilities:
-------------------------
1. Ingest raw tabular data from `data/raw/` (e.g., CSV, Excel, or JSON).
2. Standardize column names (e.g., snake_case, removal of trailing spaces).
3. Handle missing, null, or corrupted data records using domain-appropriate rules.
4. Convert date, monetary, and categorical fields into proper data types.
5. Identify and handle abnormal outliers or duplicated transactions.
6. Export the sanitized, model-ready dataset to `data/processed/`.

Note:
-----
Specific column names, schema structures, and business logic will be implemented
once our team finalizes the primary sales dataset during Day 2.
"""

import sys
from pathlib import Path
from typing import Optional
import pandas as pd


# Define project paths relative to the repository root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Load raw sales dataset from disk into a Pandas DataFrame.

    Parameters:
    -----------
    file_path : Path
        Absolute or relative Path object pointing to the raw file.

    Returns:
    --------
    pd.DataFrame
        Loaded raw dataset.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")

    print(f"[INFO] Loading raw data from: {file_path}")
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names to lowercase snake_case.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with raw column naming.

    Returns:
    --------
    pd.DataFrame
        DataFrame with standardized column names.
    """
    cleaned_df = df.copy()
    cleaned_df.columns = (
        cleaned_df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return cleaned_df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inspect and handle missing or null values according to business rules.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.

    Returns:
    --------
    pd.DataFrame
        DataFrame with missing values resolved.
    """
    cleaned_df = df.copy()
    # TODO: Implement domain-specific imputation / dropping logic once dataset schema is chosen.
    # Example:
    # cleaned_df['order_date'] = pd.to_datetime(cleaned_df['order_date'], errors='coerce')
    # cleaned_df = cleaned_df.dropna(subset=['order_id', 'order_date'])
    return cleaned_df


def handle_duplicates(df: pd.DataFrame, subset_cols: Optional[list] = None) -> pd.DataFrame:
    """
    Identify and remove duplicate records.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    subset_cols : list, optional
        Key columns used to define uniqueness (e.g., transaction ID).

    Returns:
    --------
    pd.DataFrame
        Deduplicated DataFrame.
    """
    initial_rows = len(df)
    deduped_df = df.drop_duplicates(subset=subset_cols)
    removed = initial_rows - len(deduped_df)
    if removed > 0:
        print(f"[INFO] Removed {removed} duplicate rows.")
    return deduped_df


def export_processed_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the cleaned DataFrame to the processed data directory.

    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataset.
    output_path : Path
        Destination path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Processed dataset saved to: {output_path} ({len(df)} records)")


def run_pipeline(raw_filename: str = "sales_raw.csv", output_filename: str = "sales_cleaned.csv") -> None:
    """
    Execute the end-to-end data cleaning workflow.
    """
    raw_path = RAW_DATA_DIR / raw_filename
    output_path = PROCESSED_DATA_DIR / output_filename

    print("=" * 60)
    print("Starting Sales Data Cleaning Pipeline...")
    print("=" * 60)

    try:
        raw_df = load_raw_data(raw_path)
        print(f"[INFO] Raw shape: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")

        df_std = standardize_column_names(raw_df)
        df_dedup = handle_duplicates(df_std)
        df_clean = handle_missing_values(df_dedup)

        export_processed_data(df_clean, output_path)
        print("=" * 60)
        print("Data Cleaning Pipeline completed successfully.")
        print("=" * 60)

    except FileNotFoundError:
        print(f"[WARN] Target raw file '{raw_filename}' not found in {RAW_DATA_DIR}.")
        print("[ACTION] Place the chosen raw dataset into data/raw/ to run this pipeline.")
    except Exception as exc:
        print(f"[ERROR] Pipeline execution failed: {exc}", file=sys.stderr)


if __name__ == "__main__":
    run_pipeline()
