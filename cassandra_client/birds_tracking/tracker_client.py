from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime
import time
from utils import write_log

cluster = Cluster(['172.18.0.2', '172.18.0.3', '172.18.0.4', '172.18.0.5'])
session = cluster.connect('birds')

bird_ids = [f'BIRD{i}' for i in range(1, 11)]

while True:
    for bird in bird_ids:
        date_str = datetime.utcnow().date().isoformat()
        stmt = SimpleStatement("""
            SELECT * FROM bird_tracking
            WHERE bird_id = %s AND date = %s
            LIMIT 1;
        """)
        is_traced = bird == 'BIRD1'
        result = session.execute(stmt, (bird, date_str), trace=is_traced)
        latest = result.one()
        if latest:
            log_entry = f"{datetime.utcnow()} | {bird} | {latest.latitude:.2f}, {latest.longitude:.2f}"
            print(log_entry)
            write_log(log_entry, "tracker_log.txt")
            if is_traced:
                trace = result.get_query_trace()
                if trace:
                    write_log(f"\nSELECT Trace for {bird} at {datetime.utcnow()}:", "tracker_log.txt")
                    write_log(f"Coordinator: {trace.coordinator}", "tracker_log.txt")
                    write_log(f"Duration: {trace.duration} ms", "tracker_log.txt")
                    for event in trace.events:
                        write_log(f"➡ {event.source} | {event.description} | {event.source_elapsed} µs", "tracker_log.txt")
                    print(f"Trace recorded for {bird}")
    time.sleep(2)