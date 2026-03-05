## Health Event Platform

A small event-driven healthcare data processing platform that simulates how 
clinical data flows through ingestion, validation, normalization, and persistence 
layers using Kafka and microservices.

The platform demonstrates how heterogeneous healthcare events from an 
Electronic Health Record (EHR) system can be processed through a staged 
pipeline that ensures data quality, semantic consistency, and traceability.
---
### Architecture:
The system is composed of multiple services that communicate through Kafka topics. 
Each service consumes events, processes them, and produces events for the 
next stage of the pipeline.

#### Architecture Diagram:
                                        ┌─────────────────────┐
                                        │ Fake EHR Producer   │
                                        └──────────┬──────────┘
                                                   ▼
                                           Kafka: raw-events
                                                   ▼
                                        ┌─────────────────────┐
                                        │ Validation Service  │
                                        └──────────┬──────────┘
                                                   ▼
                                        Kafka: validated-events
                                                   ▼
                                        ┌─────────────────────┐
                                        │ Normalization       │
                                        │ Service             │
                                        └──────────┬──────────┘
                                                   ▼
                                       Kafka: normalized-events
                                                   ▼
                                        ┌─────────────────────┐
                                        │ Persistence Service │
                                        └──────────┬──────────┘
                                                   ▼
                                               Database
---
### Pipeline Stages:
| Stage                     | Responsibility                                                            |
| ------------------------- | ------------------------------------------------------------------------- |
| **Fake EHR Producer**     | Simulates clinical events from an EHR system                              |
| **Validation Service**    | Validates event schema and required fields                                |
| **Normalization Service** | Transforms heterogeneous codes and formats into canonical representations |
| **Persistence Service**   | Stores normalized events for downstream consumption                       |

---
### Features
#### Event-Driven Architecture:
Services communicate asynchronously through Kafka topics, allowing independent scaling 
and loose coupling between stages.

#### Data Validation:
Incoming events are validated to ensure required structure and fields are present 
before downstream processing.

#### Semantic Normalization:
Healthcare systems often represent the same clinical concept in different ways. 
The normalization stage converts these into canonical representations.

#### Dead Letter Queue (DLQ):
Events that cannot be processed are redirected to a DLQ topic to prevent pipeline 
blockage and allow later inspection.

#### Traceability:
Events include a trace_id that propagates through the pipeline to enable 
debugging and event lineage tracking across services.

#### Shared Kafka Utilities:
Logic to check for topics creation and create if topic does not exist.

---
### Repo Structure:
```
health-event-platform
│
├── services
│   ├── config
│   │
│   ├── fake-ehr-producer
│   │   └── app
│   │   └── test
│   │
│   ├── validation-service
│   │   └── app
│   │   └── test
│   │
│   ├── normalization-service
│   │   └── app
│   │   └── test
│   │
│   ├── persistence-service
│   │   └── app
│   │   └── test
│   │
│   └── kafka-utils
│
└── docker-compose.yml
```
---
#### Services
| Service                 | Description                               |
| ----------------------- |-------------------------------------------|
| `fake-ehr-producer`     | Generates simulated clinical events       |
| `validation-service`    | Performs schema and structural validation |
| `normalization-service` | Standardizes clinical data representations |
| `persistence-service`   | Persists normalized events                |
| `kafka-utils`           | Kafka topic utilities               |
---

#### Example Event Flow

- The Fake EHR Producer generates a clinical event.
- The event is published to a Kafka raw events topic.
- The Validation Service verifies event structure.
- Valid events are published to a validated topic.
- The Normalization Service converts codes and fields into canonical formats.
- Normalized events are published to a normalized topic.
- The Persistence Service writes the event to storage.

---

#### Running the Platform
Requirements:
- Docker
- Docker Compose
- Python 3.x

Start the Platform:

From the repository root:  ``` docker-compose up --build ```

This will start:
- Kafka
- All platform services
- The simulated EHR producer