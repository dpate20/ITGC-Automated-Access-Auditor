
from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
OUTPUT_DIR = BASE_DIR / "output"

def run_script(script_name):
    """Execute a project script and return its exit code."""
    print(f"\nRunning {script_name}...", flush=True)

    result = subprocess.run(
        [sys.executable, str(SRC_DIR / script_name)],
        cwd=BASE_DIR,
        check=False
    )

    return result.returncode


def main():
    print("=== AUTOMATED ITGC AUDIT TOOLKIT ===", flush=True)
    
    # Remove reports from previous executions before starting
    report_files = [
        "termination_exceptions.csv",
        "priviledged_access_exceptions.csv",
        "data_quality_findings.csv"
    ]

    for filename in report_files:
        report_path = OUTPUT_DIR / filename

        if report_path.exists():
            report_path.unlink()

    print("Previous audit reports cleared.", flush=True)

    # First we need to validate the source data
    validation_status = run_script("data_validation.py")

    if validation_status != 0:
        print("\nAudit stopped: data validation failed.")
        return 1

    # Run termination and priviledged access control testing
    scripts = [
        "access_audit.py",
        "priviledged_access_audit.py"
    ]

    for script in scripts:
        status = run_script(script)

        if status != 0:
            print(f"\nAudit stopped: {script} failed.")
            return 1

    print("\n=== AUDIT WORKFLOW COMPLETED ===")
    print(f"Reports saved in: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
