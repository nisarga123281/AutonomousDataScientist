import pandas as pd


def calculate_data_statistics(file_path: str):
    """
    Calculate basic statistics for all numerical columns.
    """

    df = pd.read_csv(file_path)

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    statistics = {}

    for column in numerical_columns:
        statistics[column] = {
            "mean": float(df[column].mean()),
            "median": float(df[column].median()),
            "minimum": float(df[column].min()),
            "maximum": float(df[column].max()),
            "standard_deviation": float(df[column].std())
        }

    return statistics


def calculate_statistics(file_path: str):
    """
    Compatibility function used by the Phase 1 agent.
    """

    return calculate_data_statistics(file_path)