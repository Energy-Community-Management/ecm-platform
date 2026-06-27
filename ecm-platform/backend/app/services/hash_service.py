from pathlib import Path
import hashlib


class HashService:
    """Služba pro výpočet kontrolního SHA256 hashe souboru."""

    def calculate_sha256(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                sha256.update(chunk)

        return sha256.hexdigest()