import csv
import json
from pathlib import Path

import pdfplumber


def extract_text_from_pdf(filepath):
    """Extract plain text from a PDF file using pdfplumber."""
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        text_chunks = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Some pages can return None; coerce to empty string.
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)

        combined_text = "\n".join(text_chunks).strip()
        return combined_text
    except Exception as exc:
        raise RuntimeError(f"Failed to parse PDF '{file_path.name}': {exc}") from exc


def extract_text_from_txt(filepath):
    """Extract plain text from a .txt file."""
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"Text file not found: {file_path}")

    try:
        return file_path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        # Gracefully fallback if the text file is not UTF-8.
        return file_path.read_text(encoding="latin-1").strip()
    except Exception as exc:
        raise RuntimeError(f"Failed to read TXT '{file_path.name}': {exc}") from exc


def save_results_to_json(results, path):
    """Save screening results to JSON, sorted by match_score descending."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_results = sorted(results, key=lambda item: item.get("match_score", 0), reverse=True)

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(sorted_results, json_file, indent=2, ensure_ascii=False)


def save_results_to_csv(results, path):
    """Save screening results to CSV for quick inspection in spreadsheet tools."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_results = sorted(results, key=lambda item: item.get("match_score", 0), reverse=True)

    fieldnames = [
        "candidate_name",
        "match_score",
        "strengths",
        "gaps",
        "recommendation",
        "summary",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in sorted_results:
            csv_row = dict(row)
            # Store list fields in a readable delimited format for CSV.
            csv_row["strengths"] = " | ".join(csv_row.get("strengths", []))
            csv_row["gaps"] = " | ".join(csv_row.get("gaps", []))
            writer.writerow(csv_row)
