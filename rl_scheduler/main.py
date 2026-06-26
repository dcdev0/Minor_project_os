from loaders.google_trace_loader import TraceDataset
from schedulers.rr_core import run_rr
from monitoring.runtime_monitor import RuntimeMonitor

dataset = TraceDataset(
    "data/raw/part-00000-of-00500.csv"
)


dataset.load_once()


window = dataset.sample_window(1000)

print(dataset.statistics(window))

results = run_rr(
    window,
    quantum=8
)

monitor = RuntimeMonitor()

state = monitor.extract_state(results)

print("RL State:", state)

print("\n===== Runtime Statistics =====")

print(f"Average Queue Length : {results['avg_queue_length']:.2f}")

print(f"Maximum Queue Length : {results['max_queue_length']}")

print(f"Runtime CPU Utilization : {results['runtime_cpu_utilization']:.2f}")

print(f"Scheduler Cycles : {results['scheduler_cycles']}")
