# Bird Tracking System – Cassandra Cluster

## Environment Description
- Docker-based Cassandra Cluster with 4 nodes:
  - cassandra-1 (172.18.0.2)
  - cassandra-2 (172.18.0.3)
  - cassandra-3 (172.18.0.4)
  - cassandra-4 (172.18.0.5)
- Python 3.10
- Cassandra Python Driver (version ≥ 3.25)
- OS: Ubuntu 22.04 via DevContainer / VSCode

---

## Run Instructions

```bash
# Insert & Update Bird Locations
python3 cassandra_client/birds_tracking/bird_client.py

# Tracker Client: Reads latest location and writes to log
python3 cassandra_client/birds_tracking/tracker_client.py

# Node Failure Trace Test for BIRD1
python3 cassandra_client/birds_tracking/trace_bird1_test.py
````

---

## Code Files

* `bird_client.py` – Inserts and updates bird data
* `tracker_client.py` – Tracks birds and logs results
* `trace_bird1_test.py` – Performs traced operations before and after node failure
* `utils.py` – Logging helper

---

## Notes

* All clients use `trace=True` and `get_query_trace()` to extract coordinator and replica interactions.
* Replication factor: 3
* Consistency level: `LOCAL_QUORUM`

```

---
