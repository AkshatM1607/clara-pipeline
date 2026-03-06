"""Entry point to run Clara pipeline across all demo accounts."""

from __future__ import annotations

from pathlib import Path

from workflows.pipeline_a import run_pipeline_a
from workflows.pipeline_b import run_pipeline_b
from workflows.utils import ROOT_DIR


def discover_account_ids() -> list[str]:
    """Discover account IDs from data/demo/*_demo.txt filenames."""
    demo_dir = ROOT_DIR / "data" / "demo"
    account_ids: list[str] = []

    for path in sorted(demo_dir.glob("*_demo.txt")):
        account_ids.append(path.stem.replace("_demo", ""))

    return account_ids


def print_summary(results: list[tuple[str, bool, str]]) -> None:
    """Print a fixed-width summary table of pipeline execution results."""
    print("\nExecution Summary")
    print("Account     | Pipeline A | Pipeline B")
    print("------------|------------|------------")
    for account_id, a_ok, b_status in results:
        a_label = "PASS" if a_ok else "FAIL"
        print(f"{account_id:<11} | {a_label:<10} | {b_status}")


def main() -> None:
    """Run pipeline stages for each discovered account with fault tolerance."""
    account_ids = discover_account_ids()
    if not account_ids:
        print("No demo transcripts found in data/demo/. Nothing to run.")
        return

    results: list[tuple[str, bool, str]] = []

    for account_id in account_ids:
        a_ok = run_pipeline_a(account_id)

        onboarding_path = ROOT_DIR / "data" / "onboarding" / f"{account_id}_onboarding.txt"
        if onboarding_path.exists():
            if a_ok:
                b_ok = run_pipeline_b(account_id)
                b_status = "PASS" if b_ok else "FAIL"
            else:
                b_status = "SKIPPED (A failed)"
        else:
            b_status = "SKIPPED (no onboarding)"

        results.append((account_id, a_ok, b_status))

    print_summary(results)


if __name__ == "__main__":
    main()
