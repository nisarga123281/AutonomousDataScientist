from tools.insights_tools import generate_insights

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

import os
from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


def run_insights_agent(
    file_path,
    modeling_result=None
):
    """
    Phase 5 - Insights Agent

    Generates AI-based interpretation from:
    1. Dataset information
    2. Statistical information
    3. Correlation information
    4. Phase 4 modeling results
    """

    print("\n[INSIGHTS AGENT] Starting...")


    # -----------------------------------------------------
    # Generate dataset insights
    # -----------------------------------------------------

    result = generate_insights(file_path)

    if result["status"] != "success":

        return {
            "status": "error",
            "report": result.get(
                "message",
                "Unable to generate insights."
            ),
            "insights_result": result
        }


    # -----------------------------------------------------
    # Extract modeling information
    # -----------------------------------------------------

    if modeling_result is None:

        modeling_result = {}

    # Keep model result safe
    model_information = str(
        modeling_result
    )


    # -----------------------------------------------------
    # Build AI prompt
    # -----------------------------------------------------

    final_prompt = f"""
You are the Phase 5 AI Insights Agent of an
Autonomous Data Scientist system.

Your job is to interpret the dataset and the
machine learning results in a simple and useful way.

IMPORTANT RULES:

1. Use ONLY the information provided below.
2. Do not invent values.
3. Do not create fake model metrics.
4. If a value is unavailable, say "Not available".
5. Explain the findings in simple language.
6. Give practical recommendations.

DATASET INFORMATION
-------------------

Rows:
{result["rows"]}

Columns:
{result["columns"]}

Column Names:
{result["column_names"]}

Numerical Columns:
{result["numerical_columns"]}

Categorical Columns:
{result["categorical_columns"]}

Missing Values:
{result["missing_values"]}

Duplicate Rows:
{result["duplicate_rows"]}


STATISTICS
----------

{result["statistics"]}


CORRELATION
-----------

{result["correlation"]}


AUTOMATIC OBSERVATIONS
----------------------

{result["observations"]}


PHASE 4 MODELING RESULT
-----------------------

{model_information}


Create a final Phase 5 report using exactly this structure:

============================================================
AUTODS - PHASE 5 AI INSIGHTS AGENT REPORT
============================================================

DATASET SUMMARY
----------------
Explain the dataset briefly.

KEY DATA INSIGHTS
-----------------
List the important observations from the data.

STATISTICAL INSIGHTS
--------------------
Explain the important statistical findings.

CORRELATION INSIGHTS
--------------------
Explain important relationships between numerical variables.

MODEL INSIGHTS
--------------
Explain the Phase 4 model results.
If model information is unavailable, clearly say so.

IMPORTANT FINDINGS
------------------
List the most important findings.

BUSINESS / PRACTICAL INTERPRETATION
-----------------------------------
Explain what the findings mean in practical terms.

RECOMMENDATIONS
---------------
Give useful recommendations for the next stage.

NEXT STEPS
----------
Explain what should be done next in the data science workflow.

============================================================
END OF PHASE 5 AI INSIGHTS AGENT REPORT
============================================================
"""


    # -----------------------------------------------------
    # Call LLM
    # -----------------------------------------------------

    try:

        final_response = llm.invoke(
            [
                HumanMessage(
                    content=final_prompt
                )
            ]
        )

        report = final_response.content

    except Exception as e:

        print(
            f"[INSIGHTS AGENT] LLM error: {e}"
        )

        # Fallback report if LLM fails

        report = f"""
============================================================
AUTODS - PHASE 5 AI INSIGHTS AGENT REPORT
============================================================

DATASET SUMMARY
----------------
The dataset contains {result["rows"]} rows
and {result["columns"]} columns.

KEY DATA INSIGHTS
-----------------
{chr(10).join(result["observations"])}

STATISTICAL INSIGHTS
--------------------
{result["statistics"]}

CORRELATION INSIGHTS
--------------------
{result["correlation"]}

MODEL INSIGHTS
--------------
{model_information}

IMPORTANT FINDINGS
------------------
The dataset was successfully analyzed.

BUSINESS / PRACTICAL INTERPRETATION
-----------------------------------
The available statistical and modeling results
should be reviewed before making decisions.

RECOMMENDATIONS
---------------
Continue with model evaluation and validation.

NEXT STEPS
----------
Proceed to model validation and final deployment
after reviewing the results.

============================================================
END OF PHASE 5 AI INSIGHTS AGENT REPORT
============================================================
"""


    # -----------------------------------------------------
    # Return
    # -----------------------------------------------------

    return {
        "status": "success",
        "report": report,
        "insights_result": result,
        "modeling_result": modeling_result
    }