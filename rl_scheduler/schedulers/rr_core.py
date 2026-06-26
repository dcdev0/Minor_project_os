# schedulers/rr_core.py

from collections import deque
import copy


def run_rr(
    processes,
    quantum=8,
    context_switch_cost=1
):
    """
    Round Robin Scheduler

    Parameters
    ----------
    processes : list[Process]
    quantum : int
    context_switch_cost : int

    Returns
    -------
    dict
    """

    if not processes:
        return {}

    # ----------------------------------------
    # Work on a copy
    # ----------------------------------------

    processes = copy.deepcopy(processes)

    processes.sort(
        key=lambda p: p.arrival_time
    )

    current_time = 0

    ready_queue = deque()

    remaining_processes = processes[:]

    completed_processes = []

    context_switches = 0

    gantt_chart = []

    queue_length_samples = []

    cpu_busy_time = 0

    idle_time = 0

    scheduler_cycles = 0

    # ========================================
    # MAIN LOOP
    # ========================================

    while remaining_processes or ready_queue:

        # ------------------------------------
        # Add newly arrived processes
        # ------------------------------------

        while (
            remaining_processes
            and remaining_processes[0].arrival_time <= current_time
        ):

            ready_queue.append(
                remaining_processes.pop(0)
            )

            queue_length_samples.append(len(ready_queue))

        # ------------------------------------
        # CPU Idle
        # ------------------------------------

        if not ready_queue:
            if remaining_processes:

                idle_gap = (remaining_processes[0].arrival_time - current_time)

                idle_time += idle_gap

                current_time = (remaining_processes[0].arrival_time)

            scheduler_cycles += 1

            continue

        # ------------------------------------
        # Select process
        # ------------------------------------

        process = ready_queue.popleft()

        if process.response_time == -1:

            process.response_time = (
                current_time
                - process.arrival_time
            )

        start_time = current_time

        execution_time = min(
            quantum,
            process.remaining_time
        )

        cpu_busy_time += execution_time

        current_time += execution_time

        process.remaining_time -= execution_time

        gantt_chart.append(
            (
                process.pid,
                start_time,
                current_time
            )
        )

        # ------------------------------------
        # Add arrivals during execution
        # ------------------------------------

        while (
            remaining_processes
            and remaining_processes[0].arrival_time <= current_time
        ):

            ready_queue.append(
                remaining_processes.pop(0)
            )

        # ------------------------------------
        # Context Switch
        # ------------------------------------

        context_switches += 1

        current_time += context_switch_cost

        # ------------------------------------
        # Finished?
        # ------------------------------------

        if process.remaining_time > 0:

            ready_queue.append(process)

        else:

            process.completion_time = current_time

            process.turnaround_time = (
                process.completion_time
                - process.arrival_time
            )

            process.waiting_time = (
                process.turnaround_time
                - process.burst_time
            )

            completed_processes.append(process)

        scheduler_cycles += 1

    # ========================================
    # METRICS
    # ========================================

    total_processes = len(completed_processes)

    total_burst = sum(
        p.burst_time
        for p in completed_processes
    )

    avg_waiting = sum(
        p.waiting_time
        for p in completed_processes
    ) / total_processes

    avg_turnaround = sum(
        p.turnaround_time
        for p in completed_processes
    ) / total_processes

    avg_response = sum(
        p.response_time
        for p in completed_processes
    ) / total_processes

    throughput = (
        total_processes
        /
        current_time
    )

    cpu_utilization = (
        total_burst
        /
        current_time
    ) * 100

    # ========================================
# Runtime Statistics
# ========================================

    if queue_length_samples:

        avg_queue_length = (
            sum(queue_length_samples)
            / len(queue_length_samples)
        )

        max_queue_length = max(queue_length_samples)

    else:

        avg_queue_length = 0

        max_queue_length = 0

    runtime_cpu_utilization = (
        cpu_busy_time/max(1, cpu_busy_time + idle_time)) * 100

    # ========================================
    # RETURN
    # ========================================

    return {

        "quantum": quantum,

        "avg_waiting_time": avg_waiting,

        "avg_turnaround_time": avg_turnaround,

        "avg_response_time": avg_response,

        "throughput": throughput,

        "cpu_utilization": cpu_utilization,

        "context_switches": context_switches,

        "completed_processes": total_processes,

        "total_time": current_time,

        "total_burst_time": total_burst,

        "gantt_chart": gantt_chart,

        "processes": completed_processes,

        "avg_queue_length": avg_queue_length,

        "max_queue_length": max_queue_length,

        "runtime_cpu_utilization": runtime_cpu_utilization,

        "scheduler_cycles": scheduler_cycles
    }
