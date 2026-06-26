from pathlib import Path
import csv


def detect_csv_file(file_path: Path) -> dict:
    with open(file_path, mode="r", encoding="cp1250", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        rows = list(reader)
        columns = reader.fieldnames or []

    row_count = len(rows)

    if row_count <= 20 and "Celkem v intervalu" in columns:
        file_type = "MONTHLY_SUMMARY"
    elif row_count > 1000:
        file_type = "POSSIBLE_15MIN_PROFILE"
    else:
        file_type = "UNKNOWN"

    return {
        "file": file_path.name,
        "rows": row_count,
        "columns": columns,
        "type": file_type,
    }


def scan_input_folder(folder_path: Path) -> list[dict]:
    results = []

    for file_path in folder_path.glob("*.csv"):
        results.append(detect_csv_file(file_path))

    return results