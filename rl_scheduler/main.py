from loaders.google_trace_loader import TraceDataset
from environment.scheduler_env import SchedulerEnv
from rl.q_learning_agent import QLearningAgent

from training.train import train
from evaluation.evaluate import Evaluator
from evaluation.plots import Plotter

# ----------------------------------
# CHANGE ONLY THIS
# ----------------------------------

MODE = "evaluate"
# MODE = "train"

# ----------------------------------

DATASET = "data/raw/part-00000-of-00500.csv"

dataset = TraceDataset(DATASET)
dataset.load_once()

env = SchedulerEnv(
    dataset,
    window_size=1000
)

agent = QLearningAgent(
    state_bins=(5, 5, 5, 5),
    num_actions=env.num_actions()
)

# ==================================
# TRAIN
# ==================================

if MODE == "train":

    history = train(
        env,
        agent,
        episodes=1000
    )

    agent.save(
        "saved_models/q_table.npy"
    )

    plotter = Plotter()

    plotter.plot_training(
        history
    )

# ==================================
# EVALUATE
# ==================================

elif MODE == "evaluate":

    agent.load(
        "saved_models/q_table.npy"
    )

    evaluator = Evaluator(
        dataset,
        env,
        agent
    )

    results = evaluator.evaluate(
        num_windows=50
    )

    print("\n===== RESULTS =====\n")

    for scheduler in results:

        print(scheduler)

        for k, v in results[scheduler].items():

            print(f"{k}: {v}")

        print()

    plotter = Plotter()

    plotter.plot_comparison(
        results
    )
