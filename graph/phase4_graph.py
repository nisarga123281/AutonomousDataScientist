from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.modeling_agent import run_modeling_agent


class Phase4State(TypedDict, total=False):
    file_path: str
    result: dict


def modeling_node(state: Phase4State):

    file_path = state["file_path"]

    print("\n[PHASE 4 GRAPH] Running Modeling Agent")

    result = run_modeling_agent(file_path)

    return {
        "result": result
    }


graph = StateGraph(Phase4State)

graph.add_node(
    "modeling",
    modeling_node
)

graph.add_edge(
    START,
    "modeling"
)

graph.add_edge(
    "modeling",
    END
)

phase4_graph = graph.compile()