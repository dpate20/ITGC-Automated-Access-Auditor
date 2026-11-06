
import pandas as pd

from src.priviledged_access_audit import (
    find_priviledged_exceptions
)


def create_access(employee_id, enabled=True):
    return pd.DataFrame({
        "employee_id": [employee_id],
        "system_name": ["Azure"],
        "account_enabled": [enabled],
        "access_level": ["Admin"]
    })


def create_approval(employee_id, status="Approved"):
    return pd.DataFrame({
        "employee_id": [employee_id],
        "system_name": ["Azure"],
        "approved_access_level": ["Admin"],
        "approval_status": [status]
    })


def test_revoked_admin_approval():
    access = create_access("E001")
    approvals = create_approval("E001", "Revoked")

    result = find_priviledged_exceptions(
        access, approvals
    )

    assert len(result) == 1


def test_approved_admin():
    access = create_access("E002")
    approvals = create_approval("E002", "Approved")

    result = find_priviledged_exceptions(
        access, approvals
    )

    assert result.empty


def test_missing_admin_approval():
    access = create_access("E003")

    approvals = create_approval(
        "E999", "Approved"
    )

    result = find_priviledged_exceptions(
        access, approvals
    )

    assert len(result) == 1
    assert result.iloc[0]["employee_id"] == "E003"


def test_disabled_admin_account():
    access = create_access("E004", enabled=False)
    approvals = create_approval("E004", "Revoked")

    result = find_priviledged_exceptions(
        access, approvals
    )

    assert result.empty
