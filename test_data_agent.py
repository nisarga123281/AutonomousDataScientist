from agents.data_agent import run_data_agent


request = """
Analyze the CSV file data/sample.csv.
Check its rows, columns, data types,
missing values, and duplicate rows.
"""

response = run_data_agent(request)

print("\n========== DATA AGENT ==========\n")

print("AI Response:")
print(response.content)

print("\nTool Calls:")
print(response.tool_calls)