import json
from pathlib import Path
from dataclasses import asdict

from app.domain.import_record import ImportRecord


class MetadataRepository:
    """Ukládá metadata importů."""

    def __init__(self, storage_root: Path) -> None:
        self.metadata_dir = storage_root / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def save(self, record: ImportRecord) -> Path:

        file_path = self.metadata_dir / f"{record.import_id}.json"

        data = asdict(record)

        # Path → string
        data["original_file_path"] = str(record.original_file_path)
        data["stored_file_path"] = str(record.stored_file_path)

        # datetime → string
        data["imported_at"] = record.imported_at.isoformat()

        # enum → value
        data["vendor"] = record.vendor.value
        data["data_type"] = record.data_type.value
        data["file_format"] = record.file_format.value
        data["status"] = record.status.value

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return file_path