from tools.data_tools import load_dataset
from tools.profiling_tools import profile_dataset
from tools.quality_tools import check_data_quality
from tools.statistics_tools import calculate_statistics


FILE_PATH = "data/sample.csv"


print("\n========== PHASE 1: DATA UNDERSTANDING ==========\n")


# 1. Data Loading
print("1. DATA LOADING")
data_result = load_dataset(FILE_PATH)

print(f"Rows: {data_result['rows']}")
print(f"Columns: {data_result['columns']}")
print(f"Columns Names: {data_result['column_names']}")


# 2. Dataset Profiling
print("\n2. DATASET PROFILING")
profile_result = profile_dataset(FILE_PATH)

print(f"Numerical Columns: {profile_result['numerical_columns']}")
print(f"Categorical Columns: {profile_result['categorical_columns']}")
print(f"Unique Values: {profile_result['unique_values']}")


# 3. Data Quality
print("\n3. DATA QUALITY")

quality_result = check_data_quality(FILE_PATH)

print(f"Missing Values: {quality_result['missing_values']}")
print(f"Total Missing Values: {quality_result['total_missing_values']}")
print(f"Duplicate Rows: {quality_result['duplicate_rows']}")
print(f"Constant Columns: {quality_result['constant_columns']}")


# 4. Statistics
print("\n4. STATISTICS")

statistics_result = calculate_statistics(FILE_PATH)

for column, stats in statistics_result.items():
    print(f"\n{column}:")
    for name, value in stats.items():
        print(f"  {name}: {value}")


print("\n========== PHASE 1 TOOLS COMPLETED ==========\n")