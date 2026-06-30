from app.domain.energy_series import EnergySeries
from app.repositories.database import Database


class MeasurementRepository:
    """Repository pro tabulku measurements."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def save_series(
        self,
        import_id: str,
        meter_id: int,
        series: EnergySeries,
    ) -> int:
        if series.is_empty():
            return 0

        rows = [
            (
                import_id,
                meter_id,
                measurement.start.isoformat(),
                measurement.end.isoformat(),
                measurement.value_kwh,
                measurement.status,
            )
            for measurement in series
        ]

        with self.database.connect() as connection:
            connection.executemany(
                """
                INSERT INTO measurements (
                    import_id,
                    meter_id,
                    start_time,
                    end_time,
                    value_kwh,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

        return len(rows)

    def total_energy_by_import(self, import_id: str) -> float:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                SELECT COALESCE(SUM(value_kwh), 0)
                FROM measurements
                WHERE import_id = ?
                """,
                (import_id,),
            )

            return float(cursor.fetchone()[0])