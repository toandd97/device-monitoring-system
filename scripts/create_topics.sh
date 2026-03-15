#!/usr/bin/env bash
set -euo pipefail

KAFKA_BROKER="${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}"
TOPIC_NAME="${KAFKA_TOPIC_METRICS:-device.metrics.raw}"
PARTITIONS="${KAFKA_TOPIC_PARTITIONS:-8}"
REPLICATION_FACTOR="${KAFKA_TOPIC_REPLICATION_FACTOR:-1}"

echo "Creating Kafka topic '${TOPIC_NAME}' on broker '${KAFKA_BROKER}'..."

kafka-topics \
  --create \
  --if-not-exists \
  --bootstrap-server "${KAFKA_BROKER}" \
  --topic "${TOPIC_NAME}" \
  --partitions "${PARTITIONS}" \
  --replication-factor "${REPLICATION_FACTOR}"

echo "Kafka topic '${TOPIC_NAME}' is ready."

