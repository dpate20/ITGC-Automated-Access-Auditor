
from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

employees = pd.read_csv(
    DATA_DIR / "employees.csv",
    dtype={"employee_id": "string"}
)

access = pd.read_csv(
    DATA_DIR / "system_access.csv",
    dtype={"employee_id": "string"}
)

issues = []

# 1: Check any missing employee IDs or employment status
for index, row in employees.iterrows():
    if pd.isna(row["employee_id"]) or not str(row["employee_id"]).strip():
        issues.append({
            "source": "employees.csv",
            "record": index + 2,
            "issue": "Missing employee ID"
        })

    if pd.isna(row["employment_status"]) or not str(row["employment_status"]).strip():
        issues.append({
            "source": "employees.csv",
            "record": index + 2,
            "issue": "Missing employment status"
        })

# 2: Check for any duplicate employee IDs
duplicates = employees[
    employees["employee_id"].notna()
    & employees["employee_id"].duplicated(keep=False)
]

for index in duplicates.index:
    issues.append({
        "source": "employees.csv",
        "record": index + 2,
        "issue": "Duplicate employee ID"
    })

# 3: Check the account records with no matching HR employee
known_employees = set(employees["employee_id"].dropna())

for index, row in access.iterrows():
    employee_id = row["employee_id"]

    if pd.isna(employee_id) or not str(employee_id).strip():
        issues.append({
            "source": "system_access.csv",
            "record": index + 2,
            "issue": "Missing employee ID"
        })
    elif employee_id not in known_employees:
        issues.append({
            "source": "system_access.csv",
            "record": index + 2,
            "issue": "Account has no matching HR employee"
        })

# 4: Check for invalid account status
valid_values = {"true", "false"}

for index, row in access.iterrows():
    value = str(row["account_enabled"]).strip().lower()

    if value not in valid_values:
        issues.append({
            "source": "system_access.csv",
            "record": index + 2,
            "issue": "Invalid account_enabled value"
        })

# Export the data-quality report
findings = pd.DataFrame(
    issues,
    columns=["source", "record", "issue"]
)

output_file = OUTPUT_DIR / "data_quality_findings.csv"
findings.to_csv(output_file, index=False)

print("\n=== ITGC DATA QUALITY VALIDATION ===")
print(f"Employee records reviewed: {len(employees)}")
print(f"Access records reviewed: {len(access)}")
print(f"Data-quality issues identified: {len(findings)}")

if findings.empty:
    print("No data-quality issues identified.")
else:
    print(findings.to_string(index=False))

print(f"\nReport saved to: {output_file}")

if not findings.empty:
    print("\nVALIDATION FAILED: Review data-quality findings.")
    sys.exit(1)

print("\nVALIDATION PASSED: Source data checks completed.")
sys.exit(0)