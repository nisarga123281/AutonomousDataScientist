import pandas as pd


def load_data(file_path: str):
    """
    Load a CSV dataset and return basic information.
    """

    df = pd.read_csv(file_path)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum())
    }


def profile_data(file_path: str):
    """
    Profile the dataset and identify numerical,
    categorical and unique-value information.
    """

    df = pd.read_csv(file_path)

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    unique_values = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    return {
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "unique_values": unique_values
    }
    return {
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "unique_values": unique_values
    }


def load_dataset(file_path: str):
    """
    Backward-compatible alias for load_data().
    """
    return load_data(file_path)