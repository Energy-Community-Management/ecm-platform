# ECM Platform Architecture

Version: 0.1.0

---

# Přehled architektury

```
                Frontend
                    │
                    ▼
               REST API
                    │
                    ▼
             Business Services
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
   Import       Quality      Analytics
                    │
                    ▼
           Repository Manager
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 ImportRepo     MeterRepo    MeasurementRepo
                    │
                    ▼
               SQLite Database
```

---

# Domain Layer

Obsahuje čisté doménové objekty.

Například

- EnergySeries
- EnergyMeasurement
- ImportRecord
- ValidationReport
- MissingInterval

Doménová vrstva nesmí obsahovat SQL ani GUI.

---

# Service Layer

Obsahuje business logiku.

- ImportManager
- QualityService
- RepositoryManager

---

# Persistence Layer

Obsahuje

- Database
- DatabaseSchema
- ImportRepository
- MeterRepository
- MeasurementRepository

---

# Import Layer

Import dat je založen na ParserFactory.

Každý nový zdroj dat má vlastní parser.

Parser vrací jednotný objekt EnergySeries.

---

# Quality Layer

Kontrola kvality je založena na pravidlech.

Každé pravidlo je samostatná třída.

Například

- MissingIntervalRule
- DuplicateIntervalRule
- NegativeValueRule
- PowerLimitRule

---

# Analytics Layer

Analytics pracuje pouze s objektem EnergySeries.

Nikdy nepracuje přímo s databází.

---

# Návrhové principy

Projekt využívá

- SOLID
- Repository Pattern
- Service Layer
- Factory Pattern
- Domain Driven Design
- Composition over Inheritance

---

# Aktuální stav

Hotovo

✔ Import Framework

✔ Parser Factory

✔ OTE Parser

✔ EnergySeries

✔ Quality Framework

✔ SQLite Persistence

✔ Repository Manager

Rozpracováno

□ Duplicate Detection

□ Load EnergySeries

Plán

□ GoodWe

□ Sofar

□ REST API

□ Web Dashboard

□ AI Assistant