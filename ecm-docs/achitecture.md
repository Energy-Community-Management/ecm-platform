backend/
│
├── app/
│   │
│   ├── core/
│   │
│   ├── domain/
│   │   ├── enums/
│   │   ├── measurement.py
│   │   ├── energy_series.py
│   │   ├── import_record.py
│   │   ├── import_info.py
│   │   └── import_result.py
│   │
│   ├── services/
│   │   ├── import_manager.py
│   │   ├── archive_service.py
│   │   ├── hash_service.py
│   │   └── import_id_service.py
│   │
│   ├── repositories/
│   │   └── metadata_repository.py
│   │
│   ├── imports/
│   │   ├── detector.py
│   │   ├── parser_factory.py
│   │   └── parsers/
│   │       ├── ote/
│   │       ├── goodwe/
│   │       └── sofar/
│   │
│   ├── validators/
│   │
│   ├── gui/
│   │
│   └── utils/
│
├── sandbox/
│
└── storage/