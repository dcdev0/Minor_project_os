# adaptive_rr.py

from workload_analyzer import analyze_workload
from rr_scheduler import round_robin_scheduler


# =========================================================
# ADAPTIVE QUANTUM SELECTION
# =========================================================

def choose_quantum(workload_features):

    avg_burst = workload_features[
        "avg_burst_time"
    ]

    variance = workload_features[
        "burst_variance"
    ]

    arrival_density = workload_features[
        "arrival_density"
    ]

    # -----------------------------------------------------
    # HEURISTIC RULES
    # -----------------------------------------------------

    # Interactive workload
    if avg_burst <= 10:

        quantum = 4

    # Balanced workload
    elif avg_burst <= 50:

        quantum = 8

    # CPU intensive workload
    else:

        quantum = 16

    # -----------------------------------------------------
    # VARIANCE ADJUSTMENT
    # -----------------------------------------------------

    if variance > 2000:

        quantum += 4

    # -----------------------------------------------------
    # HEAVY LOAD ADJUSTMENT
    # -----------------------------------------------------

    if arrival_density > 5:

        quantum += 2

    return quantum


# =========================================================
# ADAPTIVE RR SCHEDULER
# =========================================================

def adaptive_rr_scheduler(
        processes,
        context_switch_cost=1
):

    # ---------------------------------------------
    # ANALYZE WORKLOAD
    # ---------------------------------------------

    workload_features = analyze_workload(
        processes
    )

    # ---------------------------------------------
    # CHOOSE QUANTUM
    # ---------------------------------------------

    adaptive_quantum = choose_quantum(
        workload_features
    )

    # ---------------------------------------------
    # RUN RR
    # ---------------------------------------------

    results = round_robin_scheduler(
        processes,
        time_quantum=adaptive_quantum,
        context_switch_cost=context_switch_cost
    )

    results["selected_quantum"] = (
        adaptive_quantum
    )

    results["load_type"] = (
        workload_features["load_type"]
    )

    return results
