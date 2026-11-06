
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def find_termination_exceptions(employees, access):
    """Find enabled accounts belonging to terminated employees."""

    audit_data = access.merge(
        employees,
        on="employee_id",
        how="left",
        validate="many_to_one",
        indicator=True
    )

    audit_data["employment_status"] = (
        audit_data["employment_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    audit_data["account_enabled"] = (
        audit_data["account_enabled"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    exceptions = audit_data[
        (audit_data["employment_status"] == "terminated")
        & (audit_data["account_enabled"] == "true")
    ].copy()

    exceptions["finding"] = (
        "Terminated employee has an enabled account"
    )
    exceptions["severity"] = "High"

    return exceptions


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    employees = pd.read_csv(DATA_DIR / "employees.csv")
    access = pd.read_csv(DATA_DIR / "system_access.csv")

    exceptions = find_termination_exceptions(
        employees, access
    )

    output_file = OUTPUT_DIR / "termination_exceptions.csv"
    exceptions.to_csv(output_file, index=False)

    print("\n=== ITGC USER ACCESS AUDIT ===")
    print(f"Accounts reviewed: {len(access)}")
    print(f"Potential exceptions identified: {len(exceptions)}")

    if not exceptions.empty:
        print(exceptions[
            ["employee_id", "system_name", "finding", "severity"]
        ].to_string(index=False))

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
