from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

response = llm.invoke(
    "Say hello. Tell me that you are running using Groq."
)

print("========== GROQ TEST ==========")
print(response.content)