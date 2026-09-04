from typing import TypedDict, Any
from langgraph.graph import StateGraph, END


class AutoDSState(TypedDict, total=False):
    input_file: str
    df: Any

    profiling_result: Any
    cleaning_result: Any
    eda_result: Any
    modeling_result: Any
    visualization_result: Any
    insights_result: Any
    final_report: Any


def build_autods_graph(nodes):
    graph = StateGraph(AutoDSState)

    graph.add_node("profiling", nodes["profiling"])
    graph.add_node("cleaning", nodes["cleaning"])
    graph.add_node("eda", nodes["eda"])
    graph.add_node("modeling", nodes["modeling"])
    graph.add_node("visualization", nodes["visualization"])
    graph.add_node("insights", nodes["insights"])
    graph.add_node("report", nodes["report"])

    graph.set_entry_point("profiling")

    graph.add_edge("profiling", "cleaning")
    graph.add_edge("cleaning", "eda")
    graph.add_edge("eda", "modeling")
    graph.add_edge("modeling", "visualization")
    graph.add_edge("visualization", "insights")
    graph.add_edge("insights", "report")
    graph.add_edge("report", END)

    return graph.compile()