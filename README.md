# Device Monitoring System

This project is a microservice-based system that receives, processes, and stores metrics (such as CPU, RAM, and disk usage) sent periodically from external devices.

## 🛠 Features (System Overview)
1. **Receive Metrics:** Exposes a simple REST API to receive device metrics.
2. **Message Queue:** Publishes incoming events to Apache Kafka (`device.metrics.raw`).
3. **Background Processing:** A consumer service independently processes Kafka events.
4. **Analysis & Alerts:** Analyzes metric values against thresholds and triggers alerts when values are critical.
5. **Data Storage:** Stores processing results securely in MongoDB.

## 🚀 How to Run

Running the entire system is fully automated. The application dependencies (Zookeeper, Kafka, MongoDB) and all sub-services (API and Worker) are bundled together.

Simply ensure you have **Docker** and **Docker Compose** installed on your system, and run:

```bash
docker compose up
```
*(Optionally add `-d` to run it in the background).*

**The system will automatically:**
- Start Kafka and Zookeeper
- Start MongoDB
- Initialize necessary Kafka topics (`device.metrics.raw`)
- Start the API Service
- Start the Worker Consumer Service

### 📮 API Usage:

Once the system is up and running, you can submit new device metrics to the `API_PORT` (default is `8000`):

**Endpoint:** `POST /api/v1/metrics`
```bash
curl -X POST "http://localhost:8000/api/v1/metrics" -H "Content-Type: application/json" -d '{
  "device_id": "router-01",
  "metric": "cpu_usage",
  "value": 92,
  "timestamp": "2025-12-10T10:00:00Z"
}'
```

---

## 🤖 AI Assistance & Tooling

This project and its components were developed with the assistance of **Antigravity AI**.
Leveraging models such as **Gemini Pro**, **Claude**, and **ChatGPT**.
The system was implemented following the architecture and guidelines outlined in [`implementation_plan.md`](implementation_plan.md).