from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents.visualization_agent import run_visualization_agent


# =========================================================
# STATE
# =========================================================

class Phase5State(TypedDict, total=False):

    file_path: str

    modeling_result: Any

    result: dict


# =========================================================
# VISUALIZATION NODE
# =========================================================

def visualization_node(state: Phase5State):

    print("\n" + "=" * 60)
    print("[PHASE 5] VISUALIZATION AGENT")
    print("=" * 60)

    file_path = state["file_path"]

    modeling_result = state.get(
        "modeling_result",
        {}
    )

    result = run_visualization_agent(
        file_path=file_path,
        modeling_result=modeling_result
    )

    return {
        "result": result
    }


# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(Phase5State)

builder.add_node(
    "generate_visualizations",
    visualization_node
)

builder.add_edge(
    START,
    "generate_visualizations"
)

builder.add_edge(
    "generate_visualizations",
    END
)

phase5_graph = builder.compile()