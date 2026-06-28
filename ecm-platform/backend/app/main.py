from app.services.import_manager import ImportManager


def main() -> None:
    print("=====================================")
    print(" ECM - Energy Community Management")
    print("=====================================")

    manager = ImportManager()
    validator = EnergyValidationService()

    missing = validator.find_missing_intervals(result.series)

    logger.info("Completeness: %.2f %%", validator.completeness(result.series))
    logger.info("Chybějící intervaly: %d", len(missing))

    if missing:
        logger.info("První chybějící interval:")
        logger.info("Od: %s", missing[0][0])
        logger.info("Do: %s", missing[0][1])
        logger.info("Délka: %s", missing[0][2])
    else:
        logger.info("Žádné chybějící intervaly.")

    # TODO: Spuštění GUI / API / CLI


if __name__ == "__main__":
    main()
validator = EnergyValidationService()
missing = validator.find_missing_intervals(result.series)

logger.info("Completeness: %.2f %%", validator.completeness(result.series))
logger.info("Chybějící intervaly: %d", len(missing))

if missing:
    logger.info("První chybějící interval:")
    logger.info("Od: %s", missing[0][0])
    logger.info("Do: %s", missing[0][1])
    logger.info("Délka: %s", missing[0][2])
else:
    logger.info("Žádné chybějící intervaly.")