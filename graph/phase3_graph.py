from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents.eda_agent import run_eda_agent


class Phase3State(TypedDict, total=False):
    file_path: str
    result: dict


def eda_node(state: Phase3State):

    file_path = state["file_path"]

    print("\n============================================================")
    print("[PHASE 3 GRAPH] Starting EDA Agent")
    print("============================================================")

    print("[PHASE 3 GRAPH] Using cleaned dataset:")
    print(f"[PHASE 3 GRAPH] {file_path}")

    result = run_eda_agent(file_path)

    return {
        "result": result
    }


workflow = StateGraph(Phase3State)

workflow.add_node(
    "eda",
    eda_node
)

workflow.add_edge(
    START,
    "eda"
)

workflow.add_edge(
    "eda",
    END
)

phase3_graph = workflow.compile()