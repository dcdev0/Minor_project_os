# visualization.py

import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# NORMAL PLOTS
# =========================================================

def plot_metric(
        df,
        metric,
        ylabel,
        save_name
):

    workload_types = df["workload"].unique()

    plt.figure(figsize=(8, 5))

    for workload in workload_types:

        subset = df[
            df["workload"] == workload
        ]

        plt.plot(
            subset["quantum"],
            subset[metric],
            marker='o',
            label=workload
        )

    plt.xlabel("Time Quantum")
    plt.ylabel(ylabel)

    plt.title(
        f"Quantum vs {ylabel}"
    )

    plt.legend()

    plt.grid(True)

    plt.savefig(
        f"plots/{save_name}.png"
    )

    plt.close()


# =========================================================
# NORMALIZED PLOTS
# =========================================================

def plot_normalized_metric(
        df,
        metric,
        ylabel,
        save_name
):

    workload_types = df["workload"].unique()

    plt.figure(figsize=(8, 5))

    for workload in workload_types:

        subset = df[
            df["workload"] == workload
        ].copy()

        # ---------------------------------------------
        # NORMALIZATION
        # ---------------------------------------------

        max_value = subset[metric].max()

        subset["normalized"] = (
            subset[metric] / max_value
        )

        plt.plot(
            subset["quantum"],
            subset["normalized"],
            marker='o',
            label=workload
        )

    plt.xlabel("Time Quantum")

    plt.ylabel(
        f"Normalized {ylabel}"
    )

    plt.title(
        f"Normalized Quantum vs {ylabel}"
    )

    plt.legend()

    plt.grid(True)

    plt.savefig(
        f"plots/{save_name}_normalized.png"
    )

    plt.close()


# =========================================================
# MAIN VISUALIZATION DRIVER
# =========================================================

def plot_metrics():

    df = pd.read_csv(
        "results/benchmark_results.csv"
    )

    # -----------------------------------------------------
    # STANDARD METRICS
    # -----------------------------------------------------

    metrics = [

        (
            "avg_waiting_time",
            "Average Waiting Time",
            "avg_waiting_time"
        ),

        (
            "avg_turnaround_time",
            "Average Turnaround Time",
            "avg_turnaround_time"
        ),

        (
            "avg_response_time",
            "Average Response Time",
            "avg_response_time"
        ),

        (
            "throughput",
            "Throughput",
            "throughput"
        ),

        (
            "cpu_utilization",
            "CPU Utilization",
            "cpu_utilization"
        ),

        (
            "context_switches",
            "Context Switches",
            "context_switches"
        )
    ]

    # -----------------------------------------------------
    # GENERATE ALL PLOTS
    # -----------------------------------------------------

    for metric, ylabel, save_name in metrics:

        # Normal plot
        plot_metric(
            df,
            metric,
            ylabel,
            save_name
        )

        # Normalized plot
        plot_normalized_metric(
            df,
            metric,
            ylabel,
            save_name
        )

    print("\nAll plots generated successfully.")
