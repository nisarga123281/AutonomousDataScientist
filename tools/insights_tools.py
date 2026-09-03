import pandas as pd
import os


def generate_insights(file_path):
    """
    Generate basic data insights for Phase 5.
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": f"File not found: {file_path}"
        }

    try:
        df = pd.read_csv(file_path)

        # -----------------------------
        # Basic information
        # -----------------------------

        rows = len(df)
        columns = len(df.columns)

        column_names = list(df.columns)

        numerical_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        # -----------------------------
        # Missing values
        # -----------------------------

        missing_values = int(
            df.isnull().sum().sum()
        )

        # -----------------------------
        # Duplicate rows
        # -----------------------------

        duplicate_rows = int(
            df.duplicated().sum()
        )

        # -----------------------------
        # Descriptive statistics
        # -----------------------------

        statistics = {}

        if numerical_columns:

            stats_df = df[numerical_columns].describe()

            for column in numerical_columns:

                statistics[column] = {
                    "mean": float(
                        stats_df.loc["mean", column]
                    ),
                    "median": float(
                        df[column].median()
                    ),
                    "minimum": float(
                        df[column].min()
                    ),
                    "maximum": float(
                        df[column].max()
                    ),
                    "standard_deviation": float(
                        df[column].std()
                    )
                }

        # -----------------------------
        # Correlation
        # -----------------------------

        correlation = {}

        if len(numerical_columns) >= 2:

            corr_matrix = df[
                numerical_columns
            ].corr()

            for column in numerical_columns:

                correlation[column] = {}

                for other_column in numerical_columns:

                    value = corr_matrix.loc[
                        column,
                        other_column
                    ]

                    if pd.notna(value):

                        correlation[column][
                            other_column
                        ] = float(value)

        # -----------------------------
        # Automatic observations
        # -----------------------------

        observations = []

        if missing_values == 0:

            observations.append(
                "The dataset contains no missing values."
            )

        else:

            observations.append(
                f"The dataset contains {missing_values} missing values."
            )

        if duplicate_rows == 0:

            observations.append(
                "No duplicate rows were found."
            )

        else:

            observations.append(
                f"{duplicate_rows} duplicate rows were found."
            )

        if len(numerical_columns) >= 2:

            observations.append(
                "The dataset contains multiple numerical "
                "variables, so correlation analysis can be performed."
            )

        if len(categorical_columns) > 0:

            observations.append(
                "The dataset contains categorical variables "
                "that may require encoding before machine learning."
            )

        return {
            "status": "success",
            "rows": rows,
            "columns": columns,
            "column_names": column_names,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "statistics": statistics,
            "correlation": correlation,
            "observations": observations
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }