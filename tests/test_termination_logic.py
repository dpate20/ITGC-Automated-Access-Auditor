
import pandas as pd

from src.access_audit import find_termination_exceptions


def test_terminated_user_with_enabled_account():
    employees = pd.DataFrame({
        "employee_id": ["E001"],
        "employment_status": ["Terminated"]
    })

    access = pd.DataFrame({
        "employee_id": ["E001"],
        "system_name": ["Azure"],
        "account_enabled": [True]
    })

    result = find_termination_exceptions(employees, access)

    assert len(result) == 1
    assert result.iloc[0]["employee_id"] == "E001"


def test_terminated_user_with_disabled_account():
    employees = pd.DataFrame({
        "employee_id": ["E002"],
        "employment_status": ["Terminated"]
    })

    access = pd.DataFrame({
        "employee_id": ["E002"],
        "system_name": ["Azure"],
        "account_enabled": [False]
    })

    result = find_termination_exceptions(employees, access)

    assert result.empty


def test_active_user_with_enabled_account():
    employees = pd.DataFrame({
        "employee_id": ["E003"],
        "employment_status": ["Active"]
    })

    access = pd.DataFrame({
        "employee_id": ["E003"],
        "system_name": ["Azure"],
        "account_enabled": [True]
    })

    result = find_termination_exceptions(employees, access)

    assert result.empty


def test_case_insensitive_status():
    employees = pd.DataFrame({
        "employee_id": ["E004"],
        "employment_status": [" TERMINATED "]
    })

    access = pd.DataFrame({
        "employee_id": ["E004"],
        "system_name": ["Azure"],
        "account_enabled": ["TRUE"]
    })

    result = find_termination_exceptions(employees, access)

    assert len(result) == 1
