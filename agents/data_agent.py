from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

from tools.data_tools import load_dataset


# Load environment variables
load_dotenv()


# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# Convert our Python function into a LangChain tool
@tool
def analyze_dataset(file_path: str) -> dict:
    """
    Analyze a CSV dataset and return basic information
    such as rows, columns, data types, missing values,
    and duplicate rows.
    """
    return load_dataset(file_path)


# Give the tool to Gemini
llm_with_tools = llm.bind_tools([analyze_dataset])


def run_data_agent(user_request: str):
    """
    Run the Data Agent.
    """

    response = llm_with_tools.invoke(user_request)

    return response