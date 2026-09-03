from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.report_agent import run_report_agent


class Phase6State(TypedDict, total=False):

    profiling_report: str

    cleaning_result: dict

    eda_result: dict

    modeling_result: dict

    insights_result: dict

    result: dict


def final_report_node(state: Phase6State):

    result = run_report_agent(
        profiling_report=state.get(
            "profiling_report",
            ""
        ),

        cleaning_result=state.get(
            "cleaning_result",
            {}
        ),

        eda_result=state.get(
            "eda_result",
            {}
        ),

        modeling_result=state.get(
            "modeling_result",
            {}
        ),

        insights_result=state.get(
            "insights_result",
            {}
        )
    )

    return {
        "result": result
    }


workflow = StateGraph(Phase6State)

workflow.add_node(
    "generate_final_report",
    final_report_node
)

workflow.add_edge(
    START,
    "generate_final_report"
)

workflow.add_edge(
    "generate_final_report",
    END
)

phase6_graph = workflow.compile()