from pathlib import Path

from rich.console import Console
from rich.table import Table

from screener import run_screening
from utils import save_results_to_csv, save_results_to_json


def _build_ranked_table(results):
    """Create a Rich table showing ranked candidates."""
    table = Table(title="HireLens Resume Screening Results")
    table.add_column("Rank", justify="right", style="bold")
    table.add_column("Candidate")
    table.add_column("Score", justify="right")
    table.add_column("Recommendation")
    table.add_column("Summary")

    for index, candidate in enumerate(results, start=1):
        table.add_row(
            str(index),
            candidate.get("candidate_name", "Unknown"),
            str(candidate.get("match_score", 0)),
            candidate.get("recommendation", "Not Fit"),
            candidate.get("summary", ""),
        )

    return table


def main():
    """Run end-to-end screening pipeline and persist outputs for frontend consumption."""
    console = Console()

    try:
        results, errors = run_screening()

        output_dir = Path("backend/output")
        json_path = output_dir / "results.json"
        csv_path = output_dir / "results.csv"

        save_results_to_json(results, json_path)
        save_results_to_csv(results, csv_path)

        if results:
            console.print(_build_ranked_table(results))
        else:
            console.print("[yellow]No successful candidate evaluations were produced.[/yellow]")

        console.print(f"\nSaved JSON output to: {json_path}")
        console.print(f"Saved CSV output to: {csv_path}")

        if errors:
            console.print("\n[bold yellow]Some files could not be processed:[/bold yellow]")
            for err in errors:
                console.print(f"- {err['file']}: {err['error']}")

    except Exception as exc:
        console.print(f"[bold red]HireLens failed:[/bold red] {exc}")


if __name__ == "__main__":
    main()
