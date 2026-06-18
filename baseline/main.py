# main.py

from exp_runner import run_experiments
from visualization import plot_metrics


if __name__ == "__main__":

    print("\n===================================")
    print("ROUND ROBIN BENCHMARK FRAMEWORK")
    print("===================================")

    # -------------------------------------------------
    # RUN BENCHMARKS
    # -------------------------------------------------

    run_experiments()

    # -------------------------------------------------
    # GENERATE PLOTS
    # -------------------------------------------------

    plot_metrics()

    print("\nExperiment Completed.")
