from tools.report_tools import generate_final_report


def run_report_agent(
    profiling_report="",
    cleaning_result=None,
    eda_result=None,
    modeling_result=None,
    insights_result=None
):

    print("\n" + "=" * 60)
    print("[FINAL REPORT AGENT] Starting")
    print("=" * 60)

    result = generate_final_report(
        profiling_report=profiling_report,
        cleaning_result=cleaning_result,
        eda_result=eda_result,
        modeling_result=modeling_result,
        insights_result=insights_result
    )

    print("[FINAL REPORT AGENT] Report generated successfully")

    return result