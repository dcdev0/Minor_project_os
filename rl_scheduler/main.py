from loaders.google_trace_loader import TraceDataset
from environment.scheduler_env import SchedulerEnv

dataset = TraceDataset(
    "data/raw/part-00000-of-00500.csv"
)

dataset.load_once()

env = SchedulerEnv(dataset)

state = env.reset()

print("Initial State")

print(state)

next_state, reward, done, info = env.step(3)

print()

print("Quantum")

print(env.action_to_quantum(3))

print()

print("Next State")

print(next_state)

print()

print("Reward")

print(reward)

print()

print("Done")

print(done)
