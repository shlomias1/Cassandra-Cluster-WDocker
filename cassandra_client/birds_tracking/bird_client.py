from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import time
import random
from datetime import datetime, timedelta
from utils import write_log

cluster = Cluster(['172.18.0.2', '172.18.0.3', '172.18.0.4', '172.18.0.5'])
session = cluster.connect()

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS birds
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};
""")
session.set_keyspace('birds')

session.execute("""
    CREATE TABLE IF NOT EXISTS bird_tracking (
        bird_id text,
        date text,
        timestamp timestamp,
        species text,
        latitude double,
        longitude double,
        PRIMARY KEY ((bird_id, date), timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC);
""")

bird_ids = [f'BIRD{i}' for i in range(1, 11)]
species = 'stork'

for bird in bird_ids:
    now = datetime.utcnow()
    session.execute("""
        INSERT INTO bird_tracking (bird_id, date, timestamp, species, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (bird, now.date().isoformat(), now, species, random.uniform(-90, 90), random.uniform(-180, 180)))

# Update positions for 20 steps
for i in range(20):
    for bird in bird_ids:
        now = datetime.utcnow()
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)

        # Perform trace for BIRD1 only
        trace_enabled = (bird == 'BIRD1' and i == 0)
        if trace_enabled:
            result = session.execute("""
                INSERT INTO bird_tracking (bird_id, date, timestamp, species, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (bird, now.date().isoformat(), now, species, lat, lon), trace=True)
            trace = result.get_query_trace()
            print(f"\n🛰️ INSERT Trace for {bird} at {now}:")
            print(f"Coordinator: {trace.coordinator}")
            print(f"Duration: {trace.duration} ms")
            for event in trace.events:
                print(f"➡ {event.source} | {event.description} | {event.source_elapsed} µs")
        else:
            session.execute("""
                INSERT INTO bird_tracking (bird_id, date, timestamp, species, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (bird, now.date().isoformat(), now, species, lat, lon))
        print(f"Inserted {bird} at {now}, {lat:.2f}, {lon:.2f}")
    time.sleep(1)  # simulate time gap