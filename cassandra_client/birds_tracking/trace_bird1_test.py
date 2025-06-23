from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime
import random

BIRD_ID = "BIRD1"
DATE_STR = "2025-06-22"
SPECIES = "stork"
TRACE_LOG_PATH = "trace_log.txt"

def log_trace(title, trace):
    with open(TRACE_LOG_PATH, "a") as f:
        f.write(f"\n=== {title} ===\n")
        f.write(f"Coordinator: {trace.coordinator}\n")
        f.write(f"Duration: {trace.duration} ms\n")
        for e in trace.events:
            f.write(f"{e.source} | {e.description} | {e.source_elapsed} µs\n")

def run_trace_test():
    cluster = Cluster(['172.18.0.2', '172.18.0.4', '172.18.0.5'])  # Node 3 is down
    session = cluster.connect('birds')

    # ---- UPDATE with TRACE ----
    timestamp = datetime.utcnow()
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    update_stmt = SimpleStatement("""
        INSERT INTO bird_tracking (bird_id, date, timestamp, species, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
    """)
    result = session.execute(update_stmt, (BIRD_ID, DATE_STR, timestamp, SPECIES, lat, lon), trace=True)
    trace = result.get_query_trace()

    print("\n=== UPDATE TRACE ===")
    print(f"Coordinator: {trace.coordinator}")
    print(f"Duration: {trace.duration} ms")
    for e in trace.events:
        print(f"{e.source} | {e.description} | {e.source_elapsed} µs")

    log_trace("UPDATE TRACE", trace)

    # ---- SELECT with TRACE ----
    select_stmt = SimpleStatement("""
        SELECT * FROM bird_tracking
        WHERE bird_id = %s AND date = %s
        LIMIT 1
    """)
    result = session.execute(select_stmt, (BIRD_ID, DATE_STR), trace=True)
    trace = result.get_query_trace()
    row = result.one()

    print("\n=== SELECT TRACE ===")
    if row:
        print(f"Latest Location: {row.latitude:.2f}, {row.longitude:.2f} @ {row.timestamp}")
    print(f"Coordinator: {trace.coordinator}")
    print(f"Duration: {trace.duration} ms")
    for e in trace.events:
        print(f"{e.source} | {e.description} | {e.source_elapsed} µs")

    log_trace("SELECT TRACE", trace)

if __name__ == "__main__":
    run_trace_test()