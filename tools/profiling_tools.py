import pandas as pd


def profile_dataset(file_path: str):
    """
    Create a basic profile of a CSV dataset.
    """

    df = pd.read_csv(file_path)

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    unique_values = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    return {
        "shape": {
            "rows": len(df),
            "columns": len(df.columns)
        },
        "columns": df.columns.tolist(),
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "unique_values": unique_values
    }