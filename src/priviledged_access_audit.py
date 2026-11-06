
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def find_priviledged_exceptions(access, approvals):
    """Identify enabled admin accounts without valid approval."""

    admin_accounts = access[
        access["access_level"]
        .astype("string")
        .str.strip()
        .str.lower() == "admin"
    ].copy()

    audit_data = admin_accounts.merge(
        approvals,
        on=["employee_id", "system_name"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    for column in [
        "account_enabled",
        "approval_status",
        "approved_access_level"
    ]:
        audit_data[column] = (
            audit_data[column]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    # Identify enabled admin accounts without a valid approval
    invalid_approval = (
        (audit_data["_merge"] != "both")
        | (audit_data["approval_status"] != "approved").fillna(True)
        | (audit_data["approved_access_level"] != "admin").fillna(True)
    )

    exceptions = audit_data[
        (audit_data["account_enabled"] == "true").fillna(False)
        & invalid_approval
    ].copy()

    exceptions["finding"] = (
        "Enabled admin account lacks valid approval"
    )
    exceptions["severity"] = "High"

    return exceptions


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    access = pd.read_csv(DATA_DIR / "system_access.csv")
    approvals = pd.read_csv(
        DATA_DIR / "priviledged_approvals.csv"
    )

    exceptions = find_priviledged_exceptions(
        access, approvals
    )

    output_file = (
        OUTPUT_DIR / "priviledged_access_exceptions.csv"
    )
    exceptions.to_csv(output_file, index=False)

    print("\n=== ITGC PRIVILEDGED ACCESS AUDIT ===")
    print(
        "Potential exceptions identified:",
        len(exceptions)
    )

    if not exceptions.empty:
        print(exceptions[
            ["employee_id", "system_name", "finding"]
        ].to_string(index=False))

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
