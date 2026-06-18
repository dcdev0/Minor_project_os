# main_comparison.py

from compare_plots import (
    run_comparison, plot_comparison
)

if __name__ == "__main__":

    print("\n===================================")
    print("FIXED RR vs ADAPTIVE RR")
    print("===================================")

    # -------------------------------------------------
    # RUN EXPERIMENTS
    # -------------------------------------------------

    run_comparison()

    # -------------------------------------------------
    # GENERATE PLOTS
    # -------------------------------------------------

    plot_comparison()

    print("\nComparison completed.")
