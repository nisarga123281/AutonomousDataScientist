from agents.profiling_agent import run_phase1_agent


FILE_PATH = "data/sample.csv"
OUTPUT_FILE = "outputs/phase1_report.txt"


print("\n")
print("=" * 60)
print("       AUTODS - PHASE 1 DATA UNDERSTANDING")
print("=" * 60)


# Run Phase 1 Agent
response = run_phase1_agent(FILE_PATH)


# Extract Gemini text
report = response.content


# Handle Gemini's structured content format
if isinstance(report, list):

    text_parts = []

    for item in report:

        if isinstance(item, dict) and "text" in item:
            text_parts.append(item["text"])

    report = "\n".join(text_parts)


# Display report
print("\nAI RESPONSE:\n")

print(report)


# Save report
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write(report)


print("\n")
print("=" * 60)
print("PHASE 1 REPORT SAVED")
print("=" * 60)

print(f"\nOutput file: {OUTPUT_FILE}")