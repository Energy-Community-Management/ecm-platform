# ECM Platform Coding Standards

Version: 0.1.0

---

## Základní pravidla

ECM Platform je dlouhodobý projekt. Kód musí být čitelný, modulární a rozšiřitelný.

Hlavní pravidlo:

> Jedna třída = jedna odpovědnost.

---

## Architektonická pravidla

### Domain Layer

Domain obsahuje čisté datové a doménové objekty.

Povoleno:

- dataclass
- enum
- jednoduché výpočty přímo související s objektem

Zakázáno:

- SQL
- práce se soubory
- GUI
- API
- logging
- ukládání do databáze

---

### Services

Services obsahují business logiku a orchestrace.

Příklady:

- ImportManager
- QualityService
- RepositoryManager

Services mohou používat repository, ale repository nesmí používat services.

---

### Repositories

Repositories pracují pouze s ukládáním a načítáním dat.

Příklady:

- ImportRepository
- MeterRepository
- MeasurementRepository

Repository nesmí obsahovat business logiku.

---

### Imports

Parser pouze převádí vstupní data na doménové objekty.

Parser nesmí:

- ukládat data
- zapisovat do databáze
- řešit kvalitu dat
- počítat sdílení energie

---

### Quality

Quality modul kontroluje kvalitu dat pomocí pravidel.

Každé pravidlo musí být samostatná třída.

Příklad:

- MissingIntervalRule
- DuplicateIntervalRule
- NegativeValueRule

---

## Naming conventions

### Soubory

Používat snake_case.

Správně:

```text
quality_service.py
measurement_repository.py
missing_interval_rule.py