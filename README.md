# ITGC Automated Access Auditor

A Python-based IT General Controls (ITGC) auditing tool designed to automate user access reconciliation, identify potential access-control exceptions, and validate source data before performing audit tests.

The project demonstrates practical applications of Python, Pandas, identity and access management (IAM), and automated IT control testing.

## Overview

The tool reconciles synthetic HR employee records, system access listings, and privileged access approvals to identify potential security control exceptions.

It performs three primary operations:

1. **Data Quality Validation:** Identifies missing, duplicated, or unmatched records and invalid account-enabled values.
2. **User Termination Access Testing:** Identifies terminated employees who retain enabled system accounts.
3. **Privileged Access Testing:** Identifies enabled administrator accounts without valid approval records.

The tool produces CSV reports containing potential exceptions requiring further investigation.

## Technologies Used

- Python 3
- Pandas
- pytest
- CSV
- Git and GitHub

## Audit Workflow

```text
Employee Records ────────┐
                         |
System Access Records ───┼──> Data Validation
                         |          |
Privileged Approvals ────┘          |
                                    v
                           Validation Passed?
                              /         \
                            No           Yes
                            |             |
                       Stop Audit         v
                                  Termination Access Test
                                           |
                                           v
                                  Privileged Access Test
                                           |
                                           v
                                    CSV Audit Reports
```

## Control Tests

### ITGC-01: User Termination Access Review

Compares HR employment records against system access records to identify terminated employees with enabled accounts.

**Example finding:** A terminated employee retains an enabled Azure account.

### ITGC-02: Privileged Access Authorization

Compares administrative system accounts against documented access approval records.

**Example finding:** An enabled administrator account has a revoked or missing approval.

### ITGC-03: Data Quality Validation

Checks source datasets for missing employee identifiers, duplicate HR employee IDs, unmatched access records, missing employment statuses, and invalid account-enabled values.

If a defined validation issue is detected, the audit workflow stops before executing the control tests.

## Installation

Clone the repository:

```bash
git clone https://github.com/dpate20/ITGC-Automated-Access-Auditor.git
cd ITGC-Automated-Access-Auditor
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the complete audit:

```bash
python src/run_audit.py
```

The program validates the source data and, if validation succeeds, runs both access-control tests.

Generated reports are saved in the `output/` directory:

- `data_quality_findings.csv`
- `termination_exceptions.csv`
- `privileged_access_exceptions.csv`

## Example Results

Using the included synthetic dataset:

| Control Test | Records Reviewed | Potential Exceptions |
|---|---:|---:|
| Data Quality Validation | 5 employee records, 5 access records | 0 |
| Termination Access Review | 5 access records | 1 |
| Privileged Access Review | 2 administrator accounts | 1 |

Both access-control findings relate to the same fictional employee, E002.

The sample results demonstrate that the tool can identify an enabled account belonging to a terminated employee and an administrator account with revoked access approval.

## Automated Testing

The project uses pytest to validate detection logic and expected report outputs.

Run:

```bash
python src/run_audit.py
python -m pytest -v
```

**Latest verified test execution: 12 passed, 0 failed.**

The tests cover termination-access scenarios, approved and revoked privileged access, missing approvals, disabled accounts, and normalization of employment status values.

## Failure Handling

The workflow stops when defined critical data-quality issues are detected.

Before execution, previously generated CSV reports are cleared from the current output directory to prevent stale findings from being mistaken for current results.

The data-quality report remains available when validation fails.

## Limitations

- The project uses synthetic data and does not connect directly to enterprise identity providers.
- Findings represent potential control exceptions requiring human investigation.
- Data validation covers selected known conditions rather than comprehensive evidence reliability.
- Existing report-validation tests depend on generated CSV files.
- Access approval testing does not yet evaluate approval expiration dates or full historical authorization periods.
- The project is an educational audit automation prototype, not a production-ready GRC platform.

## Future Improvements

- Expand source-data validation and exception handling.
- Integrate Microsoft Graph for authorized Entra ID access reviews.
- Add time-based termination and approval testing.
- Implement run-specific report folders and historical audit trails.
- Generate consolidated audit summaries and risk reports.
- Integrate automated testing with GitHub Actions.

## Security and Ethics

All example datasets contain fictional employee and system-access information.

This project does not contain proprietary company data, real employee access records, confidential audit workpapers, or privileged credentials.

**Author:** Devarth Patel

**GitHub:** [dpate20](https://github.com/dpate20)
