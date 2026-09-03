def generate_final_report(
    profiling_report="",
    cleaning_result=None,
    eda_result=None,
    modeling_result=None,
    insights_result=None
):

    # ------------------------------------------------------------
    # Make sure dictionaries are available
    # ------------------------------------------------------------

    cleaning_result = cleaning_result or {}
    eda_result = eda_result or {}
    modeling_result = modeling_result or {}
    insights_result = insights_result or {}

    # ------------------------------------------------------------
    # FINAL REPORT
    # ------------------------------------------------------------

    report = f"""
============================================================
AUTODS - FINAL DATA SCIENCE REPORT
============================================================

1. DATASET OVERVIEW
-------------------
Rows analyzed       : {eda_result.get("rows", "Not available")}
Columns             : {eda_result.get("columns", "Not available")}
Column names        : {eda_result.get("column_names", [])}

2. DATA QUALITY
----------------
Missing values      : {eda_result.get("missing_values", "Not available")}
Duplicate rows      : {insights_result.get("duplicate_rows", "Not available")}

3. CLEANING SUMMARY
-------------------
Original rows       : {cleaning_result.get("original_rows", "Not available")}
Cleaned rows        : {cleaning_result.get("cleaned_rows", "Not available")}
Duplicates removed  : {cleaning_result.get("duplicates_removed", "Not available")}
Missing before      : {cleaning_result.get("missing_values_before", "Not available")}
Missing after       : {cleaning_result.get("missing_values_after", "Not available")}

Cleaned file        : {cleaning_result.get("cleaned_file", "Not available")}

4. EXPLORATORY DATA ANALYSIS
----------------------------
Numerical columns   : {eda_result.get("numerical_columns", [])}
Categorical columns : {eda_result.get("categorical_columns", [])}

Statistics:
{eda_result.get("statistics", "Not available")}

Correlation:
{eda_result.get("correlation", "Not available")}

Outliers:
{eda_result.get("outliers", "Not available")}

5. MODELING
-----------
Algorithm           : {modeling_result.get("algorithm", "Linear Regression")}
Feature             : {modeling_result.get("feature", "Not available")}
Target              : {modeling_result.get("target", "Not available")}

Training rows       : {modeling_result.get("training_rows", "Not available")}
Testing rows        : {modeling_result.get("testing_rows", "Not available")}

MAE                 : {modeling_result.get("mae", "Not available")}
RMSE                : {modeling_result.get("rmse", "Not available")}
R2 Score            : {modeling_result.get("r2_score", "Not available")}

Coefficient         : {modeling_result.get("coefficient", "Not available")}
Intercept           : {modeling_result.get("intercept", "Not available")}

6. AI INSIGHTS
--------------
{insights_result.get("observations", "No additional observations available.")}

7. IMPORTANT FINDINGS
---------------------
"""

    # ------------------------------------------------------------
    # CORRELATION FINDING
    # ------------------------------------------------------------

    correlation = eda_result.get(
        "correlation",
        {}
    )

    if isinstance(correlation, dict):

        try:

            columns = list(correlation.keys())

            if len(columns) >= 2:

                col1 = columns[0]
                col2 = columns[1]

                value = correlation[col1].get(
                    col2
                )

                if value is not None:

                    report += (
                        f"\n- Correlation between "
                        f"{col1} and {col2} "
                        f"is approximately {value:.3f}."
                    )

        except Exception:

            pass

    # ------------------------------------------------------------
    # R2 FINDING
    # ------------------------------------------------------------

    r2 = modeling_result.get(
        "r2_score"
    )

    if r2 is not None:

        report += (
            f"\n- The model achieved an R² score "
            f"of approximately {r2:.3f}."
        )

    # ------------------------------------------------------------
    # COEFFICIENT FINDING
    # ------------------------------------------------------------

    coefficient = modeling_result.get(
        "coefficient"
    )

    if coefficient is not None:

        report += (
            f"\n- The model coefficient is "
            f"approximately {coefficient:.3f}."
        )

    # ------------------------------------------------------------
    # CLEANING FINDING
    # ------------------------------------------------------------

    duplicates_removed = cleaning_result.get(
        "duplicates_removed"
    )

    if duplicates_removed is not None:

        if duplicates_removed > 0:

            report += (
                f"\n- {duplicates_removed} duplicate "
                f"row(s) were removed during cleaning."
            )

        else:

            report += (
                "\n- No duplicate rows were removed "
                "during cleaning."
            )

    # ------------------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------------------

    report += """

8. RECOMMENDATIONS
------------------
1. Validate the model using additional unseen datasets.
2. Perform cross-validation to check model stability.
3. Compare multiple machine learning algorithms.
4. Add more useful features when available.
5. Monitor model performance after deployment.

9. FINAL CONCLUSION
-------------------
The AutoDS pipeline successfully processed the dataset through
profiling, cleaning, EDA, modeling and AI insight generation.

The cleaned dataset was used for downstream analysis,
including EDA and modeling.

The final analysis can be used as a starting point for further
data science and machine learning work.

10. NEXT STEPS
--------------
1. Feature engineering
2. Cross-validation
3. Algorithm comparison
4. Model deployment
5. Model monitoring

============================================================
END OF AUTODS FINAL DATA SCIENCE REPORT
============================================================
"""

    # ------------------------------------------------------------
    # RETURN RESULT
    # ------------------------------------------------------------

    return {

        "status": "success",

        "report": report

    }
