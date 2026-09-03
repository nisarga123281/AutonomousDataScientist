import pandas as pd
import os


def perform_eda(file_path: str):
    """
    Perform Exploratory Data Analysis on the given CSV file.

    IMPORTANT:
    This function analyzes exactly the file_path received
    from the previous phase.
    """

    # ============================================================
    # STEP 1 - CHECK FILE
    # ============================================================

    if not file_path:
        raise ValueError(
            "EDA received an empty file path."
        )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"EDA file not found: {file_path}"
        )

    print("\n" + "=" * 60)
    print("[EDA TOOL] Reading dataset")
    print("=" * 60)

    print(
        f"[EDA TOOL] File being analyzed: {file_path}"
    )

    # ============================================================
    # STEP 2 - LOAD DATASET
    # ============================================================

    df = pd.read_csv(file_path)

    print(
        f"[EDA TOOL] Rows loaded    : {len(df)}"
    )

    print(
        f"[EDA TOOL] Columns loaded : {len(df.columns)}"
    )

    print(
        f"[EDA TOOL] Columns        : {list(df.columns)}"
    )

    # ============================================================
    # BASIC INFORMATION
    # ============================================================

    rows = len(df)

    columns = len(df.columns)

    column_names = list(df.columns)

    # ============================================================
    # NUMERICAL COLUMNS
    # ============================================================

    numerical_columns = list(
        df.select_dtypes(
            include=["int64", "float64"]
        ).columns
    )

    # ============================================================
    # CATEGORICAL COLUMNS
    # ============================================================

    categorical_columns = list(
        df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns
    )

    # ============================================================
    # DESCRIPTIVE STATISTICS
    # ============================================================

    statistics = {}

    for column in numerical_columns:

        statistics[column] = {

            "mean":
                float(df[column].mean()),

            "median":
                float(df[column].median()),

            "minimum":
                float(df[column].min()),

            "maximum":
                float(df[column].max()),

            "standard_deviation":
                float(df[column].std())

        }

    # ============================================================
    # CORRELATION
    # ============================================================

    correlation = {}

    if len(numerical_columns) > 1:

        corr_df = df[
            numerical_columns
        ].corr()

        for column in corr_df.columns:

            correlation[column] = {}

            for other_column in corr_df.columns:

                correlation[column][other_column] = float(
                    corr_df.loc[
                        column,
                        other_column
                    ]
                )

    # ============================================================
    # MISSING VALUES
    # ============================================================

    missing_values = {}

    for column in df.columns:

        missing_values[column] = int(
            df[column].isna().sum()
        )

    # ============================================================
    # UNIQUE VALUES
    # ============================================================

    unique_values = {}

    for column in df.columns:

        unique_values[column] = int(
            df[column].nunique()
        )

    # ============================================================
    # OUTLIER DETECTION
    # IQR METHOD
    # ============================================================

    outliers = {}

    for column in numerical_columns:

        Q1 = df[column].quantile(0.25)

        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR

        upper_bound = Q3 + 1.5 * IQR

        outlier_count = int(
            (
                (df[column] < lower_bound)
                |
                (df[column] > upper_bound)
            ).sum()
        )

        outliers[column] = {

            "count":
                outlier_count,

            "lower_bound":
                float(lower_bound),

            "upper_bound":
                float(upper_bound)

        }

    # ============================================================
    # FINAL RESULT
    # ============================================================

    result = {

        "status":
            "success",

        "file_path":
            file_path,

        "rows":
            rows,

        "columns":
            columns,

        "column_names":
            column_names,

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns,

        "missing_values":
            missing_values,

        "unique_values":
            unique_values,

        "statistics":
            statistics,

        "correlation":
            correlation,

        "outliers":
            outliers

    }

    print("\n[EDA TOOL] Analysis completed.")

    print(
        f"[EDA TOOL] Final row count: {rows}"
    )

    return result


def run_eda(file_path: str):
    """
    Compatibility function for Phase 3.
    """

    return perform_eda(file_path)
