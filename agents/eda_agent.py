from tools.eda_tools import perform_eda


def run_eda_agent(file_path: str):
    """
    Phase 3 EDA Agent.

    Performs EDA on the exact dataset received
    from the orchestrator.
    """

    print("\n[EDA AGENT] Starting EDA...")

    print(
        f"[EDA AGENT] Input file: {file_path}"
    )

    # ============================================================
    # STEP 1 - RUN EDA TOOL
    # ============================================================

    print(
        "[EDA AGENT] Running tool: perform_eda"
    )

    result = perform_eda(
        file_path
    )

    print(
        f"[EDA AGENT] Rows analyzed: {result['rows']}"
    )

    print(
        f"[EDA AGENT] Columns analyzed: {result['columns']}"
    )

    # ============================================================
    # STEP 2 - STATISTICS TEXT
    # ============================================================

    statistics_text = ""

    for column, values in result["statistics"].items():

        statistics_text += f"""
{column}
  Mean               : {values["mean"]:.4f}
  Median             : {values["median"]:.4f}
  Minimum            : {values["minimum"]:.4f}
  Maximum            : {values["maximum"]:.4f}
  Standard Deviation : {values["standard_deviation"]:.4f}
"""

    # ============================================================
    # STEP 3 - CORRELATION TEXT
    # ============================================================

    correlation_text = ""

    if result["correlation"]:

        for column, correlations in result[
            "correlation"
        ].items():

            for other_column, value in correlations.items():

                if column <= other_column:

                    correlation_text += (
                        f"{column} vs {other_column} : "
                        f"{value:.4f}\n"
                    )

    else:

        correlation_text = (
            "Correlation analysis requires "
            "at least two numerical columns."
        )

    # ============================================================
    # STEP 4 - OUTLIER TEXT
    # ============================================================

    outlier_text = ""

    for column, values in result[
        "outliers"
    ].items():

        outlier_text += (
            f"{column} : "
            f"{values['count']} outliers "
            f"(lower={values['lower_bound']:.4f}, "
            f"upper={values['upper_bound']:.4f})\n"
        )

    # ============================================================
    # STEP 5 - MISSING VALUES
    # ============================================================

    missing_text = ""

    for column, count in result[
        "missing_values"
    ].items():

        missing_text += (
            f"{column} : {count}\n"
        )

    # ============================================================
    # STEP 6 - UNIQUE VALUES
    # ============================================================

    unique_text = ""

    for column, count in result[
        "unique_values"
    ].items():

        unique_text += (
            f"{column} : {count}\n"
        )

    # ============================================================
    # STEP 7 - REPORT
    # ============================================================

    report = f"""
============================================================
AUTODS - PHASE 3 EDA AGENT REPORT
============================================================

EDA STATUS
----------
Exploratory Data Analysis completed successfully.

INPUT DATASET
-------------
File             : {file_path}

DATASET OVERVIEW
----------------
Rows             : {result["rows"]}
Columns          : {result["columns"]}
Column Names     : {", ".join(result["column_names"])}

NUMERICAL COLUMNS
-----------------
{", ".join(result["numerical_columns"]) if result["numerical_columns"] else "None"}

CATEGORICAL COLUMNS
-------------------
{", ".join(result["categorical_columns"]) if result["categorical_columns"] else "None"}

DESCRIPTIVE STATISTICS
----------------------
{statistics_text}

MISSING VALUES
--------------
{missing_text}

UNIQUE VALUES
-------------
{unique_text}

CORRELATION ANALYSIS
--------------------
{correlation_text}

OUTLIER ANALYSIS
----------------
{outlier_text}

KEY FINDINGS
------------
1. The cleaned dataset contains {result["rows"]} observations.
2. The dataset contains {result["columns"]} columns.
3. Numerical columns were analyzed using descriptive statistics.
4. Correlation analysis was performed between numerical variables.
5. Outliers were checked using the IQR method.
6. Missing values were checked for every column.

RECOMMENDATIONS
---------------
1. Examine the correlation between numerical variables.
2. Investigate detected outliers before modeling.
3. Use suitable visualizations such as histograms and scatter plots.
4. Consider the relationship between Experience and Salary.
5. Use the EDA results to guide the next modeling phase.

============================================================
END OF PHASE 3 EDA AGENT
============================================================
"""

    print(
        "\n[EDA AGENT] EDA completed successfully."
    )

    # ============================================================
    # RETURN
    # ============================================================

    return {

        "status":
            "success",

        "file_path":
            file_path,

        "report":
            report,

        "eda_result":
            result

    }
