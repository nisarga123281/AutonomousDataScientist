from tools.modeling_tools import train_regression_model


def run_modeling_agent(file_path: str):
    """
    Run Phase 4 Modeling Agent.
    """

    print("\n" + "=" * 60)
    print("[MODELING AGENT] Starting Phase 4")
    print("=" * 60)

    print(f"[MODELING AGENT] Dataset: {file_path}")

    # Run modeling tool
    result = train_regression_model(file_path)

    print("[MODELING AGENT] Model training completed")

    report = f"""
============================================================
AUTODS - PHASE 4 MODELING AGENT REPORT
============================================================

MODELING STATUS
---------------
Regression model trained successfully.

DATASET
-------
Rows Used          : {result["rows"]}
Feature            : {result["feature"]}
Target             : {result["target"]}

DATA SPLIT
----------
Training Rows      : {result["training_rows"]}
Testing Rows       : {result["testing_rows"]}

MODEL
-----
Algorithm          : Linear Regression

MODEL PARAMETERS
----------------
Coefficient        : {result["coefficient"]:.4f}
Intercept          : {result["intercept"]:.4f}

MODEL PERFORMANCE
-----------------
MAE                : {result["mae"]:.4f}
RMSE               : {result["rmse"]:.4f}
R2 Score           : {result["r2_score"]:.4f}

KEY FINDINGS
------------
1. The cleaned dataset was successfully loaded.
2. Numerical columns were identified.
3. The first numerical column was used as the feature.
4. The second numerical column was used as the target.
5. The data was divided into training and testing sets.
6. A Linear Regression model was trained.
7. Predictions were generated for the test data.
8. MAE, RMSE and R2 Score were calculated.

RECOMMENDATION
--------------
Use the model performance metrics to determine whether
Linear Regression is suitable for this dataset.

============================================================
END OF PHASE 4 MODELING AGENT REPORT
============================================================
"""

    return {
        "status": "success",
        "report": report,
        "modeling_result": result
    }