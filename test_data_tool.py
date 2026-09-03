from tools.data_tools import load_dataset


file_path = "data/sample.csv"

result = load_dataset(file_path)

print("\n========== DATASET ANALYSIS ==========\n")

for key, value in result.items():
    print(f"{key}: {value}")