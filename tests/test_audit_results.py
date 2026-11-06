
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def test_termination_exception():
    """A terminated employee with an enabled account is flagged."""

    findings = pd.read_csv(
        OUTPUT_DIR / "termination_exceptions.csv"
    )

    assert len(findings) == 1
    assert findings.iloc[0]["employee_id"] == "E002"
    assert findings.iloc[0]["system_name"] == "Azure"


def test_priviledged_access_exception():
    """An enabled admin account with revoked approval is flagged."""

    findings = pd.read_csv(
        OUTPUT_DIR / "priviledged_access_exceptions.csv"
    )

    assert len(findings) == 1
    assert findings.iloc[0]["employee_id"] == "E002"
    assert findings.iloc[0]["approval_status"].lower() == "revoked"


def test_approved_admin_not_flagged():
    """An approved administrator should not appear in the findings."""

    findings = pd.read_csv(
        OUTPUT_DIR / "priviledged_access_exceptions.csv"
    )

    assert "E005" not in findings["employee_id"].values


def test_disabled_terminated_account_not_flagged():
    """A disabled account belonging to a terminated user should pass."""

    findings = pd.read_csv(
        OUTPUT_DIR / "termination_exceptions.csv"
    )

    assert "E004" not in findings["employee_id"].values
