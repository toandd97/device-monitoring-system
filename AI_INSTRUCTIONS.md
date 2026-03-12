You are a senior backend engineer.

Generate a production-ready Python microservice project for a device monitoring system.

Follow clean architecture and OOP design.

IMPORTANT:
The project structure must follow this style:

config
src

Inside src use modules like:

controllers
services
models
common
validators
kafka
database

This structure is required.

--------------------------------------------------

SYSTEM OVERVIEW

Devices periodically send metrics such as CPU usage, RAM usage, disk usage.

The backend system must:

1. Receive metrics through REST API
2. Publish events to Kafka
3. Consume Kafka events
4. Analyze metric values against thresholds
5. Store results in MongoDB
6. Trigger alerts when values are critical

--------------------------------------------------

TECH STACK

Language:
Python

Framework:
FastAPI

Message Queue:
Kafka

Database:
MongoDB

Container:
Docker + Docker Compose

--------------------------------------------------

PROJECT STRUCTURE

Use this project structure:

device-monitoring-system
│
├── config
│   ├── settings.py
│   ├── kafka_config.py
│   ├── mongo_config.py
│
├── src
│   │
│   ├── controllers
│   │   └── metric_controller.py
│   │
│   ├── services
│   │   └── metric_service.py
│   │
│   ├── models
│   │   └── metric_model.py
│   │
│   ├── validators
│   │   └── metric_validator.py
│   │
│   ├── kafka
│   │   ├── producer.py
│   │   └── consumer.py
│   │
│   ├── database
│   │   ├── mongo_connection.py
│   │   └── base_model.py
│   │
│   ├── common
│   │   ├── response.py
│   │   ├── logger.py
│   │   └── utils.py
│   │
│   └── main.py
│
├── scripts
│   ├── create_topics.sh
│   └── init_env.sh
│
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md

--------------------------------------------------

API REQUIREMENTS

Endpoint:

POST /api/v1/metrics

Example request:

{
  "device_id": "router-01",
  "metric": "cpu_usage",
  "value": 92,
  "timestamp": "2025-12-10T10:00:00Z"
}

The API must:

- validate input
- publish event to Kafka

--------------------------------------------------

EVENT MESSAGE FORMAT

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

--------------------------------------------------

KAFKA REQUIREMENTS

Kafka topic:

device.metrics.raw

Partitions:

8

Provide script:

scripts/create_topics.sh

The script must create the Kafka topic automatically.

--------------------------------------------------

DATABASE

MongoDB collection:

metrics

Example document:

{
  "_id": "uuid",
  "device_id": "router-01",
  "metric": "cpu_usage",
  "value": 92,
  "status": "CRITICAL",
  "timestamp": "ISO8601"
}

--------------------------------------------------

DATABASE LAYER

Create reusable MongoDB layer.

mongo_connection.py

Must implement:

connect
get_collection
close

Create base_model.py with reusable functions:

insert_one
find_one
find_all
find_with_fields
update_one
delete_one

Use OOP.

--------------------------------------------------

KAFKA LAYER

Create Kafka classes:

producer.py
consumer.py

Producer must support:

connect
publish_event

Consumer must support:

consume events
commit offsets

--------------------------------------------------

VALIDATION

Create validators for API input.

Check:

device_id required
metric required
value numeric
timestamp ISO format

--------------------------------------------------

RESPONSE HANDLER

Create common/response.py

Functions:

success_response()
error_response()

--------------------------------------------------

ENVIRONMENT VARIABLES

Create .env.example

Variables:

KAFKA_BOOTSTRAP_SERVERS
KAFKA_TOPIC_METRICS
MONGO_URI
API_PORT

Create script:

scripts/init_env.sh

This script generates .env automatically.

--------------------------------------------------

DOCKER COMPOSE

docker-compose.yml must include:

zookeeper
kafka
mongo
app service

Kafka must run with port 9092.

--------------------------------------------------

AUTOMATION

Running the system should only require:

docker compose up

The system must automatically:

start kafka
start mongo
create kafka topic
start API service

--------------------------------------------------

CODE QUALITY

Requirements:

- OOP design
- clear module separation
- logging
- error handling
- reusable components

--------------------------------------------------

OUTPUT FORMAT

1. Show full folder structure
2. Generate all code files
3. Generate docker-compose.yml
4. Generate shell scripts
5. Generate README