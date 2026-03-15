#!/bin/sh

echo "[init] Waiting for Kafka..."

cub kafka-ready -b kafka:9092 1 60

echo "[init] Creating topic..."

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic device.metrics.raw \
  --partitions 8 \
  --replication-factor 1

echo "[init] Kafka topic ready"