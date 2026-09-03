import pandas as pd


def check_data_quality(file_path: str):
    """
    Check a dataset for common data-quality problems.
    """

    df = pd.read_csv(file_path)

    missing_values = df.isnull().sum()

    missing_values = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    duplicate_rows = int(df.duplicated().sum())

    constant_columns = [
        column
        for column in df.columns
        if df[column].nunique(dropna=False) <= 1
    ]

    return {
        "missing_values": missing_values,
        "total_missing_values": sum(missing_values.values()),
        "duplicate_rows": duplicate_rows,
        "constant_columns": constant_columns
    }