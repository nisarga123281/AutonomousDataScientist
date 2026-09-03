from tools.cleaning_tools import clean_dataset


def run_cleaning_agent(file_path: str):
    """
    Phase 2 - Cleaning Agent

    Cleans the dataset and generates a simple cleaning report.
    """

    print("\n[CLEANING AGENT] Running tool: clean_dataset")

    # Run cleaning tool
    result = clean_dataset(file_path)

    print("[CLEANING AGENT] Tool result:")
    print(result)

    # Check whether cleaning was successful
    if result.get("status") != "success":
        return {
            "status": "failed",
            "report": "Dataset cleaning failed.",
            "details": result
        }

    # Create Phase 2 report
    report = f"""
============================================================
AUTODS - PHASE 2 CLEANING AGENT REPORT
============================================================

CLEANING STATUS
---------------
Dataset cleaning completed successfully.

DATASET CLEANING SUMMARY
------------------------
Original Rows       : {result.get("original_rows", "N/A")}
Cleaned Rows        : {result.get("cleaned_rows", "N/A")}
Duplicates Removed  : {result.get("duplicates_removed", "N/A")}

MISSING VALUES
--------------
Before Cleaning     : {result.get("missing_values_before", "N/A")}
After Cleaning      : {result.get("missing_values_after", "N/A")}

CLEANED DATASET
---------------
File: {result.get("cleaned_file", "N/A")}

KEY FINDINGS
------------
1. The dataset was successfully loaded.
2. Duplicate rows were checked and removed.
3. Missing values were checked.
4. The cleaned dataset was saved successfully.
5. The cleaned dataset is ready for the next phase.

RECOMMENDATION
--------------
Use the cleaned dataset for further analysis and modeling.

============================================================
END OF PHASE 2 CLEANING AGENT REPORT
============================================================
"""

    return {
        "status": "success",
        "report": report,
        "cleaning_result": result
    }
