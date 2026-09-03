from graph.phase1_graph import phase1_graph


FILE_PATH = "data/experience_salary_120.csv"


result = phase1_graph.invoke({
    "file_path": FILE_PATH
})


print()
print("=" * 60)
print("             AUTODS - PROFILING AGENT")
print("=" * 60)

print()
print("STATUS:")
print(result["status"])

print()
print("FILE:")
print(result["file_path"])

print()
print("DATA QUALITY FLAGS:")
print("Has Missing Values:", result["has_missing_values"])
print("Has Duplicates:", result["has_duplicates"])

print()
print("PROFILING AGENT REPORT:")
print(result["report"])

print()
print("=" * 60)
print("          PROFILING AGENT COMPLETE")
print("=" * 60)