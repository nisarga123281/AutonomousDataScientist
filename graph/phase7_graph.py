from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.orchestrator_agent import run_autods_pipeline


class Phase7State(TypedDict, total=False):

    file_path: str
    result: dict


def autods_node(state: Phase7State):

    file_path = state["file_path"]

    print("\n============================================================")
    print("[PHASE 7] Autonomous Orchestrator Starting")
    print("============================================================")

    result = run_autods_pipeline(file_path)

    return {
        "result": result
    }


# ============================================================
# CREATE LANGGRAPH
# ============================================================

workflow = StateGraph(Phase7State)

workflow.add_node(
    "autods",
    autods_node
)

workflow.add_edge(
    START,
    "autods"
)

workflow.add_edge(
    "autods",
    END
)

phase7_graph = workflow.compile()
