#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"

if [ -f "${ENV_FILE}" ]; then
  echo ".env already exists, skipping generation."
  exit 0
fi

cat > "${ENV_FILE}" <<EOF
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC_METRICS=device.metrics.raw
MONGO_URI=mongodb://mongo:27017
MONGO_DB_NAME=device_monitoring
API_PORT=8000
EOF

echo "Generated ${ENV_FILE}"

