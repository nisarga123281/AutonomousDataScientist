from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.profiling_agent import run_phase1_agent
from tools.data_tools import load_data, profile_data
from tools.quality_tools import check_data_quality
from tools.statistics_tools import calculate_data_statistics
from agents.profiling_agent import run_phase1_agent

class Phase1State(TypedDict, total=False):
    file_path: str

    data_info: dict
    profile_info: dict
    quality_info: dict
    statistics_info: dict

    has_missing_values: bool
    has_duplicates: bool

    report: str
    status: str


# ============================================================
# NODE 1 - LOAD DATA
# ============================================================

def load_data_node(state: Phase1State):

    result = load_data(state["file_path"])

    return {
        "data_info": result
    }


# ============================================================
# NODE 2 - PROFILE DATA
# ============================================================

def profile_data_node(state: Phase1State):

    result = profile_data(state["file_path"])

    return {
        "profile_info": result
    }


# ============================================================
# NODE 3 - DATA QUALITY
# ============================================================

def quality_check_node(state: Phase1State):

    result = check_data_quality(state["file_path"])

    has_missing_values = (
        result.get("total_missing_values", 0) > 0
    )

    has_duplicates = (
        result.get("duplicate_rows", 0) > 0
    )

    return {
        "quality_info": result,
        "has_missing_values": has_missing_values,
        "has_duplicates": has_duplicates
    }


# ============================================================
# NODE 4 - STATISTICS
# ============================================================

def statistics_node(state: Phase1State):

    result = calculate_data_statistics(
        state["file_path"]
    )

    return {
        "statistics_info": result
    }


# ============================================================
# NODE 5 - AI REPORT
# ============================================================

def report_node(state: Phase1State):

    result = run_phase1_agent(
        file_path=state["file_path"]
    )

    return {
        "report": result,
        "status": "completed"
    }


# ============================================================
# CREATE LANGGRAPH WORKFLOW
# ============================================================

workflow = StateGraph(Phase1State)


workflow.add_node(
    "load_data",
    load_data_node
)

workflow.add_node(
    "profile_data",
    profile_data_node
)

workflow.add_node(
    "quality_check",
    quality_check_node
)

workflow.add_node(
    "statistics",
    statistics_node
)

workflow.add_node(
    "generate_report",
    report_node
)


# ============================================================
# WORKFLOW FLOW
# ============================================================

workflow.set_entry_point("load_data")

workflow.add_edge(
    "load_data",
    "profile_data"
)

workflow.add_edge(
    "profile_data",
    "quality_check"
)

workflow.add_edge(
    "quality_check",
    "statistics"
)

workflow.add_edge(
    "statistics",
    "generate_report"
)

workflow.add_edge(
    "generate_report",
    END
)


# ============================================================
# COMPILE
# ============================================================

phase1_graph = workflow.compile()