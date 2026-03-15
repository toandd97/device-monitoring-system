#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"

touch "${ENV_FILE}"

ensure_var() {
  local key="$1"
  local value="$2"
  if grep -qE "^${key}=" "${ENV_FILE}"; then
    return 0
  fi
  echo "${key}=${value}" >> "${ENV_FILE}"
}

echo "Generating default .env values (if missing)..."

# --- Core Database & Kafka ---
ensure_var "KAFKA_BOOTSTRAP_SERVERS" "kafka:9092"
ensure_var "KAFKA_TOPIC_METRICS" "device.metrics.raw"
ensure_var "MONGO_URI" "mongodb://mongo:27017"
ensure_var "MONGO_DB_NAME" "device_monitoring"
ensure_var "API_PORT" "8000"

# --- Services toggles (simulator and consumer) ---
ensure_var "SCHEDULER_ENABLED" "true"
ensure_var "SCHEDULER_INTERVAL_SECONDS" "5"
ensure_var "CONSUMER_ENABLED" "true"

# --- Alarm configurations ---
# You can override these in the .env file with your real Chat ID and Bot Token
ensure_var "ALERT_TELEGRAM_TOKEN" ""
ensure_var "ALERT_TELEGRAM_CHAT_ID" ""
ensure_var "DISCORD_WEBHOOK_URL" ""

echo "Done! Please edit '${ENV_FILE}' with your actual Telegram or Discord configurations."

