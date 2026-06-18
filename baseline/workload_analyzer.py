# workload_analyzer.py

import statistics


# =========================================================
# WORKLOAD ANALYZER
# =========================================================

def analyze_workload(processes):

    burst_times = [
        p.burst_time for p in processes
    ]

    arrival_times = [
        p.arrival_time for p in processes
    ]

    # -----------------------------------------------------
    # BASIC STATISTICS
    # -----------------------------------------------------

    avg_burst_time = statistics.mean(
        burst_times
    )

    burst_variance = statistics.variance(
        burst_times
    )

    max_burst = max(burst_times)

    min_burst = min(burst_times)

    # -----------------------------------------------------
    # WORKLOAD DISTRIBUTION
    # -----------------------------------------------------

    small_jobs = len([
        b for b in burst_times
        if b <= 10
    ])

    medium_jobs = len([
        b for b in burst_times
        if 10 < b <= 50
    ])

    large_jobs = len([
        b for b in burst_times
        if b > 50
    ])

    total_jobs = len(processes)

    small_ratio = small_jobs / total_jobs
    medium_ratio = medium_jobs / total_jobs
    large_ratio = large_jobs / total_jobs

    # -----------------------------------------------------
    # ARRIVAL DENSITY
    # -----------------------------------------------------

    arrival_span = (
        max(arrival_times) -
        min(arrival_times) + 1
    )

    arrival_density = (
        total_jobs / arrival_span
    )

    # -----------------------------------------------------
    # LOAD CLASSIFICATION
    # -----------------------------------------------------

    if avg_burst_time <= 10:

        load_type = "interactive"

    elif avg_burst_time <= 50:

        load_type = "balanced"

    else:

        load_type = "cpu_intensive"

    # -----------------------------------------------------
    # RETURN FEATURES
    # -----------------------------------------------------

    return {

        "avg_burst_time": avg_burst_time,

        "burst_variance": burst_variance,

        "min_burst": min_burst,

        "max_burst": max_burst,

        "arrival_density": arrival_density,

        "small_job_ratio": small_ratio,

        "medium_job_ratio": medium_ratio,

        "large_job_ratio": large_ratio,

        "load_type": load_type
    }
