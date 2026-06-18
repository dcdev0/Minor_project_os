# experiment_runner.py

import pandas as pd

from dataset_generator import generate_dataset
from rr_scheduler import round_robin_scheduler


def run_experiments():

    workload_types = [
        "small",
        "medium",
        "large",
        "mixed"
    ]

    all_results = []

    for workload in workload_types:

        print(f"\nRunning workload: {workload}")

        dataset = generate_dataset(
            num_processes=200,
            workload_type=workload
        )

        for quantum in range(1, 101, 5):

            result = round_robin_scheduler(
                dataset,
                time_quantum=quantum,
                context_switch_cost=1
            )

            result["workload"] = workload

            all_results.append(result)

            print(
                f"Q={quantum} "
                f"| WT={result['avg_waiting_time']:.2f}"
            )

    # -----------------------------------------------------
    # SAVE RESULTS
    # -----------------------------------------------------

    df = pd.DataFrame(all_results)

    df.to_csv(
        "results/benchmark_results.csv",
        index=False
    )

    print("\nResults saved successfully.")
