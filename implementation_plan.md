# Device Monitoring System - Implementation Plan

## 1. System Overview
The Device Monitoring System is a production-ready microservice designed to handle periodic metrics (CPU usage, RAM usage, disk usage) sent by various devices. 

The backend system is responsible for:
1. Receiving metrics through a REST API.
2. Publishing events to a Kafka message queue.
3. Consuming Kafka events for processing.
4. Analyzing metric values against predefined thresholds.
5. Storing the processed results in MongoDB.
6. Triggering alerts when metric values hit critical levels.

## 2. Tech Stack
- **Language**: Python
- **Framework**: FastAPI
- **Message Queue**: Kafka
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose

## 3. Project Structure
The project follows a clean architecture and Object-Oriented Programming (OOP) design.

```text
device-monitoring-system
│
├── config/              # Configuration files (settings, Kafka, Mongo)
├── src/
│   ├── controllers/     # API route handlers
│   ├── services/        # Business logic (e.g., threshold analysis)
│   ├── models/          # Data models and structures
│   ├── validators/      # Input validation logic
│   ├── kafka/           # Kafka producer and consumer clients
│   ├── database/        # MongoDB connection and base operations
│   ├── common/          # Shared utilities (responses, loggers)
│   └── main.py          # FastAPI application entry point
├── scripts/             # Initialization and setup scripts
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## 4. API Requirements

**Endpoint:** `POST /api/v1/metrics`

**Example Request:**
```json
{
  "device_id": "router-01",
  "metric": "cpu_usage",
  "value": 92,
  "timestamp": "2025-12-10T10:00:00Z"
}
```

**Responsibilities:**
- Validate API input (device_id, metric, numeric value, ISO format timestamp).
- Publish a standardized event to the configured Kafka topic.
- Return a standardized success/error response.

## 5. Event Driven Architecture (Kafka)

**Topic:** `device.metrics.raw` (8 partitions)

**Event Message Format:**
```json
{
  "event_id": "uuid",
  "event_type": "metric.reported",
  "timestamp": "ISO8601",
  "source": "ingestion-service",
  "payload": {
    "device_id": "router-01",
    "metric": "cpu_usage",
    "value": 92
  }
}
```

**Producer functionality:**
- Connect to the Kafka broker.
- Publish `metric.reported` events.

**Consumer functionality:**
- Connect to the Kafka broker.
- Consume events from `device.metrics.raw`.
- Process the events and commit offsets.

## 6. Database Layer (MongoDB)

**Collection:** `metrics`

**Example Document:**
```json
{
  "_id": "uuid",
  "event_id": "uuid",
  "event_type": "metric.reported",
  "timestamp": "ISO8601",
  "source": "ingestion-service",
  "payload": {
    "device_id": "router-01",
    "metric": "cpu_usage",
    "value": 92,
    "status": "CRITICAL"
  },
  "created_time": "ISO8601",
  "updated_time": "ISO8601"
}
```

**Database Wrapper (`base_model.py`):**
- Provides reusable OOP operations: `insert_one`, `find_one`, `find_all`, `find_with_fields`, `update_one`, `delete_one`.

## 7. Deployment & Automation
- Environment variables configured via `.env` (bootstrapped from `.env.example`).
- Docker Compose orchestrates Zookeeper, Kafka (port 9092), MongoDB, and the API Service.
- Startup is fully automated via `docker compose up`, bringing up all dependencies and the application simultaneously.
