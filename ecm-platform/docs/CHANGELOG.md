# Changelog

## v0.1.0 - Initial Architecture

Release Date: 2026-06-30

### Added

- Import Framework
- Parser Factory
- OTE Parser
- EnergySeries
- Analytics
- Quality Framework
- SQLite Persistence
- Database Schema
- Repository Pattern
- Repository Manager

### Architecture

- Layered Architecture
- Repository Pattern
- Service Layer
- Factory Pattern

### Notes

První stabilní architektonická verze backendu ECM Platform.


## v0.2.0 - Import Management

### Added

- Duplicate import detection by SHA256 checksum
- Import history listing
- Open existing import by ID
- Load existing EnergySeries from database
- ImportSummary domain object
- ImportSummaryService
- ImportStatistics domain object
- ImportStatisticsService
- Demo scripts for import history and import statistics

### Changed

- Improved duplicate import workflow
- Duplicate import now returns existing import details
- RepositoryManager now works as persistence facade

### Notes

This version completes the first Import Management layer of ECM Platform.