db = db.getSiblingDB("device_monitoring");

db.device_metrics.createIndex(
  { device_id: 1, timestamp: -1 },
  { name: "idx_device_time" }
);

print("Mongo index ready");