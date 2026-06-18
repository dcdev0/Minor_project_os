# compare_fixed_vs_adaptive.py

import pandas as pd
import matplotlib.pyplot as plt

from dataset_generator import generate_dataset

from rr_scheduler import round_robin_scheduler

from adaptive_rr import adaptive_rr_scheduler


# =========================================================
# RUN COMPARISON
# =========================================================

def run_comparison():

    workload_types = [
        "small",
        "medium",
        "large",
        "mixed"
    ]

    fixed_quantum = 8

    results = []

    for workload in workload_types:

        print(f"\nTesting workload: {workload}")

        dataset = generate_dataset(
            num_processes=200,
            workload_type=workload
        )

        # -------------------------------------------------
        # FIXED RR
        # -------------------------------------------------

        fixed_results = round_robin_scheduler(
            dataset,
            time_quantum=fixed_quantum,
            context_switch_cost=1
        )

        fixed_results["scheduler"] = (
            "Fixed RR"
        )

        fixed_results["workload"] = workload

        results.append(fixed_results)

        # -------------------------------------------------
        # ADAPTIVE RR
        # -------------------------------------------------

        adaptive_results = adaptive_rr_scheduler(
            dataset,
            context_switch_cost=1
        )

        adaptive_results["scheduler"] = (
            "Adaptive RR"
        )

        adaptive_results["workload"] = workload

        results.append(adaptive_results)

    # -----------------------------------------------------
    # SAVE RESULTS
    # -----------------------------------------------------

    df = pd.DataFrame(results)

    df.to_csv(
        "results/fixed_vs_adaptive.csv",
        index=False
    )

    print("\nComparison results saved.")


# =========================================================
# COMPARISON PLOTS
# =========================================================

def plot_comparison():

    df = pd.read_csv(
        "results/fixed_vs_adaptive.csv"
    )

    metrics = [

        "avg_waiting_time",

        "avg_turnaround_time",

        "avg_response_time",

        "throughput",

        "context_switches"
    ]

    for metric in metrics:

        plt.figure(figsize=(8, 5))

        for scheduler in df["scheduler"].unique():

            subset = df[
                df["scheduler"] == scheduler
            ]

            plt.bar(
                subset["workload"] + "_" + scheduler,
                subset[metric],
                label=scheduler
            )

        plt.xticks(rotation=30)

        plt.ylabel(metric)

        plt.title(
            f"Fixed RR vs Adaptive RR\n({metric})"
        )

        plt.tight_layout()

        plt.savefig(
            f"plots/comparison_{metric}.png"
        )

        plt.close()

    print("\nComparison plots generated.")
