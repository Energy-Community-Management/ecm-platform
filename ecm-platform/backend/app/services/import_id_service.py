from datetime import datetime


class ImportIdService:
    """Generuje ID importu."""

    def generate(self) -> str:
        now = datetime.now()
        return f"IMP-{now.strftime('%Y%m%d-%H%M%S')}"