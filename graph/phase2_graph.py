from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.cleaning_agent import run_cleaning_agent


class Phase2State(TypedDict):
    file_path: str
    result: dict


def cleaning_node(state: Phase2State):

    file_path = state["file_path"]

    result = run_cleaning_agent(file_path)

    return {
        "file_path": file_path,
        "result": result
    }


# ---------------------------------------
# Create Phase 2 Graph
# ---------------------------------------

workflow = StateGraph(Phase2State)

workflow.add_node(
    "cleaning_agent",
    cleaning_node
)

workflow.set_entry_point("cleaning_agent")

workflow.add_edge(
    "cleaning_agent",
    END
)

phase2_graph = workflow.compile()