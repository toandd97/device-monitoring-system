#!/usr/bin/env sh

set -e

KAFKA_BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}"
KAFKA_TOPIC_METRICS="${KAFKA_TOPIC_METRICS:-device.metrics.raw}"
KAFKA_TOPIC_PARTITIONS="${KAFKA_TOPIC_PARTITIONS:-8}"
KAFKA_TOPIC_REPLICATION_FACTOR="${KAFKA_TOPIC_REPLICATION_FACTOR:-1}"
KAFKA_TOPICS_SCRIPT="${KAFKA_TOPICS_SCRIPT:-/usr/bin/kafka-topics}"

wait_for_kafka() {
  echo "[init] Waiting for Kafka at ${KAFKA_BOOTSTRAP_SERVERS}..."
  max=60
  i=0
  while [ $i -lt $max ]; do
    if "$KAFKA_TOPICS_SCRIPT" --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --list 1>/dev/null 2>&1; then
      echo "[init] Kafka is ready."
      return 0
    fi
    i=$((i + 1))
    sleep 2
  done
  echo "[init] ERROR: Kafka did not become ready in time."
  return 1
}

# ---- Kafka: tạo topic ----
create_kafka_topics() {
  echo "[init] Creating Kafka topic '${KAFKA_TOPIC_METRICS}'..."
  "$KAFKA_TOPICS_SCRIPT" --create --if-not-exists \
    --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" \
    --topic "$KAFKA_TOPIC_METRICS" \
    --partitions "$KAFKA_TOPIC_PARTITIONS" \
    --replication-factor "$KAFKA_TOPIC_REPLICATION_FACTOR"
  echo "[init] Topic '${KAFKA_TOPIC_METRICS}' ready."
}


# ---- Main ----
wait_for_kafka
create_kafka_topics


echo "[init] All init steps completed."
