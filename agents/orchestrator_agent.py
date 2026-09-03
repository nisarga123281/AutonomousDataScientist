from graph.phase1_graph import phase1_graph
from graph.phase2_graph import phase2_graph
from graph.phase3_graph import phase3_graph
from graph.phase4_graph import phase4_graph
from graph.phase5_graph import phase5_graph
from graph.phase6_graph import phase6_graph


def run_autods_pipeline(file_path):

    print("\n" + "=" * 60)
    print("AUTODS - AUTONOMOUS PIPELINE")
    print("=" * 60)

    # ============================================================
    # PHASE 1 - PROFILING
    # ============================================================

    print("\n[PHASE 1] Profiling...")

    phase1_result = phase1_graph.invoke({
        "file_path": file_path,
        "report": "",
        "status": "",
        "rows": 0,
        "columns": 0,
        "has_missing_values": False,
        "has_duplicates": False
    })

    print("[PHASE 1] Profiling completed.")

    # ============================================================
    # PHASE 2 - CLEANING
    # ============================================================

    print("\n[PHASE 2] Cleaning...")

    phase2_result = phase2_graph.invoke({
        "file_path": file_path,
        "result": {}
    })

    phase2_data = phase2_result.get(
        "result",
        {}
    )

    # ------------------------------------------------------------
    # Get actual cleaning result
    # ------------------------------------------------------------

    if "cleaning_result" in phase2_data:

        cleaning_result = phase2_data["cleaning_result"]

    else:

        cleaning_result = phase2_data

    print("[PHASE 2] Cleaning completed.")

    # ============================================================
    # SELECT CLEANED DATASET
    # ============================================================

    cleaned_file = cleaning_result.get(
        "cleaned_file"
    )

    if cleaned_file:

        eda_path = cleaned_file

        print(
            "\n[AUTODS] Cleaned dataset found:"
        )

        print(
            f"[AUTODS] Using: {eda_path}"
        )

    else:

        eda_path = file_path

        print(
            "\n[AUTODS] WARNING: Cleaned dataset not found."
        )

        print(
            f"[AUTODS] Using original file: {eda_path}"
        )

    # ============================================================
    # PHASE 3 - EDA
    # ============================================================

    print("\n[PHASE 3] Exploratory Data Analysis...")
    print(
        f"[PHASE 3] Input dataset: {eda_path}"
    )

    phase3_result = phase3_graph.invoke({
        "file_path": eda_path
    })

    phase3_data = phase3_result.get(
        "result",
        {}
    )

    if "eda_result" in phase3_data:

        eda_result = phase3_data["eda_result"]

    else:

        eda_result = phase3_data

    print("[PHASE 3] EDA completed.")

    # ============================================================
    # PHASE 4 - MODELING
    # ============================================================

    print("\n[PHASE 4] Modeling...")
    print(
        f"[PHASE 4] Input dataset: {eda_path}"
    )

    phase4_result = phase4_graph.invoke({
        "file_path": eda_path
    })

    phase4_data = phase4_result.get(
        "result",
        {}
    )

    if "modeling_result" in phase4_data:

        modeling_result = phase4_data["modeling_result"]

    else:

        modeling_result = phase4_data

    print("[PHASE 4] Modeling completed.")

    # ============================================================
    # PHASE 5 - AI INSIGHTS
    # ============================================================

    print("\n[PHASE 5] AI Insights...")
    print(
        f"[PHASE 5] Input dataset: {eda_path}"
    )

    phase5_result = phase5_graph.invoke({

        "file_path": eda_path,

        "modeling_result": modeling_result

    })

    phase5_data = phase5_result.get(
        "result",
        {}
    )

    if "insights_result" in phase5_data:

        insights_result = phase5_data["insights_result"]

    else:

        insights_result = phase5_data

    print("[PHASE 5] AI Insights completed.")

    # ============================================================
    # PHASE 6 - FINAL REPORT
    # ============================================================

    print("\n[PHASE 6] Final Report...")

    phase6_result = phase6_graph.invoke({

        "profiling_report":
            phase1_result.get(
                "report",
                ""
            ),

        "cleaning_result":
            cleaning_result,

        "eda_result":
            eda_result,

        "modeling_result":
            modeling_result,

        "insights_result":
            insights_result

    })

    phase6_data = phase6_result.get(
        "result",
        {}
    )

    final_report = phase6_data.get(
        "report",
        ""
    )

    print("[PHASE 6] Final Report completed.")

    # ============================================================
    # PIPELINE COMPLETED
    # ============================================================

    print("\n" + "=" * 60)
    print("AUTODS PIPELINE COMPLETED")
    print("=" * 60)

    # ============================================================
    # FINAL RESULT
    # ============================================================

    return {

        "status": "success",

        "workflow_status": "completed",

        "input_file": file_path,

        "analysis_file": eda_path,

        "phases": {

            "phase1_profiling":
                "completed",

            "phase2_cleaning":
                "completed",

            "phase3_eda":
                "completed",

            "phase4_modeling":
                "completed",

            "phase5_ai_insights":
                "completed",

            "phase6_final_report":
                "completed"

        },

        "profiling_result":
            phase1_result,

        "cleaning_result":
            cleaning_result,

        "eda_result":
            eda_result,

        "modeling_result":
            modeling_result,

        "insights_result":
            insights_result,

        "final_report":
            final_report

    }
