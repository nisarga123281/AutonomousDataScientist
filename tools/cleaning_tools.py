import pandas as pd
import os


def clean_dataset(file_path: str):
    """
    Clean dataset for Phase 2.
    """

    # Load dataset
    df = pd.read_csv(file_path)

    # Original information
    original_rows = len(df)

    # Count duplicates
    duplicate_count = int(df.duplicated().sum())

    # Count missing values
    missing_before = int(df.isnull().sum().sum())

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    for column in df.columns:

        if df[column].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(df[column]):

                # Fill numeric missing values with median
                df[column] = df[column].fillna(
                    df[column].median()
                )

            else:

                # Fill categorical missing values with mode
                mode = df[column].mode()

                if not mode.empty:
                    df[column] = df[column].fillna(mode[0])

    # Count missing values after cleaning
    missing_after = int(df.isnull().sum().sum())

    # Create cleaned filename
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    name, extension = os.path.splitext(filename)

    cleaned_file = os.path.join(
        directory,
        name + "_cleaned" + extension
    )

    # Save cleaned dataset
    df.to_csv(cleaned_file, index=False)

    return {
        "status": "success",
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "duplicates_removed": duplicate_count,
        "missing_values_before": missing_before,
        "missing_values_after": missing_after,
        "cleaned_file": cleaned_file
    }