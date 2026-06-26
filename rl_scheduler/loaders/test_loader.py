from loaders.google_trace_loader import load_trace

processes = load_trace(
    "data/raw/part-00000-of-00500.csv",
    max_tasks=10
)

print("\nLoaded Tasks\n")

for p in processes:

    print(
        p.pid,
        p.arrival_time,
        p.burst_time,
        p.cpu_request,
        p.memory_request
    )

print(
    f"Loaded {len(processes)} tasks "
    f"from Google Trace"
)
