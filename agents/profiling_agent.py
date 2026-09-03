from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

from tools.data_tools import load_dataset
from tools.profiling_tools import profile_dataset
from tools.quality_tools import check_data_quality
from tools.statistics_tools import calculate_statistics


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ============================================================
# PHASE 1 TOOLS
# ============================================================

@tool
def load_data(file_path: str):
    """Load a CSV dataset and return basic information."""
    return load_dataset(file_path)


@tool
def profile_data(file_path: str):
    """Profile the dataset and identify columns and data types."""
    return profile_dataset(file_path)


@tool
def check_quality(file_path: str):
    """Check missing values, duplicates and constant columns."""
    return check_data_quality(file_path)


@tool
def calculate_data_statistics(file_path: str):
    """Calculate numerical statistics."""
    return calculate_statistics(file_path)


# ============================================================
# TOOL LIST
# ============================================================

tools = [
    load_data,
    profile_data,
    check_quality,
    calculate_data_statistics
]


# ============================================================
# TOOL LOOKUP
# ============================================================

tool_map = {
    "load_data": load_data,
    "profile_data": profile_data,
    "check_quality": check_quality,
    "calculate_data_statistics": calculate_data_statistics
}


# ============================================================
# BIND TOOLS TO GROQ
# ============================================================

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# PROFILING AGENT
# ============================================================

def run_phase1_agent(file_path: str):

    request = f"""
You are the Phase 1 Profiling Agent
of an Autonomous Data Scientist.

Analyze this dataset:

{file_path}

Your responsibilities are:

1. Load the dataset.
2. Identify number of rows and columns.
3. Identify numerical columns.
4. Identify categorical columns.
5. Identify data types.
6. Identify unique values.
7. Check missing values.
8. Check duplicate rows.
9. Check constant columns.
10. Calculate numerical statistics.
11. Analyze all tool results.

IMPORTANT:
You MUST use the tools to get the actual information.

You MUST use the calculate_data_statistics tool
to obtain:

- mean
- median
- minimum
- maximum
- standard deviation

Do NOT invent statistics.

After collecting the tool results, create a
FINAL PHASE 1 PROFILING REPORT.
"""

    # ========================================================
    # FIRST LLM CALL
    # ========================================================

    response = llm_with_tools.invoke(request)

    # ========================================================
    # STORE MESSAGES
    # ========================================================

    messages = [
        HumanMessage(content=request),
        response
    ]

    # ========================================================
    # EXECUTE ALL REQUESTED TOOLS
    # ========================================================

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\n[PROFILING AGENT] Running tool: {tool_name}")

        selected_tool = tool_map[tool_name]

        tool_result = selected_tool.invoke(tool_args)

        print(f"[PROFILING AGENT] Tool result: {tool_result}")

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

    # ==========================================
    # FINAL REPORT
    # ==========================================

    tool_results_text = ""

    for item in messages:
        tool_results_text += f"\n{str(item)}\n"


    final_prompt = f"""
    You are the Phase 1 Profiling Agent of AutoDS.

    Create the final profiling report for this dataset:

    FILE:
    {file_path}

    IMPORTANT:
    You already have all required information below.
    DO NOT call any tools.
    DO NOT try to open files.
    DO NOT use repo_browser.
    DO NOT request additional information.
    Only analyze the information provided below.

    TOOL RESULTS:
    {tool_results_text}

    Create the final report using exactly this structure:

    ==================================================
    AUTODS - PROFILING AGENT REPORT
    ==================================================

    DATASET OVERVIEW
    ----------------
    Explain the number of rows, columns, column names and data types.

    NUMERICAL COLUMNS
    -----------------
    List the numerical columns and their statistics.

    CATEGORICAL COLUMNS
    -------------------
    List categorical columns.
    If there are none, clearly say "None".

    DATA QUALITY
    ------------
    Report:
    - Missing values
    - Duplicate rows
    - Constant columns

    STATISTICS
    ----------
    For every numerical column provide:
    - Mean
    - Median
    - Minimum
    - Maximum
    - Standard deviation

    KEY FINDINGS
    ------------
    Give important observations from the dataset.

    RECOMMENDATIONS
    ---------------
    Give practical recommendations for the next stage.

    ==================================================
    END OF PROFILING AGENT REPORT
    ==================================================

    Use ONLY the tool results provided above.
    Do not invent any values.
    """


    # IMPORTANT:
    # Use the normal LLM, NOT llm_with_tools
    final_response = llm.invoke(final_prompt)

    return final_response