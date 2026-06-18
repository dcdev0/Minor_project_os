# rr_scheduler.py

from collections import deque
import copy


def round_robin_scheduler(
        processes,
        time_quantum=4,
        context_switch_cost=1
):

    processes = copy.deepcopy(processes)

    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0

    ready_queue = deque()

    remaining_processes = processes[:]

    completed_processes = []

    context_switches = 0

    gantt_chart = []

    while remaining_processes or ready_queue:

        # -------------------------------------------------
        # ADD ARRIVED PROCESSES
        # -------------------------------------------------

        while (
                remaining_processes and
                remaining_processes[0].arrival_time <= current_time
        ):

            ready_queue.append(
                remaining_processes.pop(0)
            )

        # -------------------------------------------------
        # CPU IDLE
        # -------------------------------------------------

        if not ready_queue:

            current_time += 1
            continue

        # -------------------------------------------------
        # SELECT PROCESS
        # -------------------------------------------------

        process = ready_queue.popleft()

        # Response time
        if process.response_time == -1:

            process.response_time = (
                current_time - process.arrival_time
            )

        start_time = current_time

        execution_time = min(
            time_quantum,
            process.remaining_time
        )

        current_time += execution_time

        process.remaining_time -= execution_time

        gantt_chart.append(
            (process.pid, start_time, current_time)
        )

        # -------------------------------------------------
        # ADD NEW ARRIVALS DURING EXECUTION
        # -------------------------------------------------

        while (
                remaining_processes and
                remaining_processes[0].arrival_time <= current_time
        ):

            ready_queue.append(
                remaining_processes.pop(0)
            )

        # -------------------------------------------------
        # CONTEXT SWITCH
        # -------------------------------------------------

        context_switches += 1
        current_time += context_switch_cost

        # -------------------------------------------------
        # PROCESS COMPLETE?
        # -------------------------------------------------

        if process.remaining_time > 0:

            ready_queue.append(process)

        else:

            process.completion_time = current_time

            process.turnaround_time = (
                process.completion_time -
                process.arrival_time
            )

            process.waiting_time = (
                process.turnaround_time -
                process.burst_time
            )

            completed_processes.append(process)

    # =====================================================
    # METRICS
    # =====================================================

    avg_waiting_time = (
        sum(p.waiting_time for p in completed_processes)
        / len(completed_processes)
    )

    avg_turnaround_time = (
        sum(p.turnaround_time for p in completed_processes)
        / len(completed_processes)
    )

    avg_response_time = (
        sum(p.response_time for p in completed_processes)
        / len(completed_processes)
    )

    total_burst_time = sum(
        p.burst_time for p in completed_processes
    )

    cpu_utilization = (
        total_burst_time / current_time
    ) * 100

    throughput = (
        len(completed_processes) / current_time
    )

    return {
        "quantum": time_quantum,
        "avg_waiting_time": avg_waiting_time,
        "avg_turnaround_time": avg_turnaround_time,
        "avg_response_time": avg_response_time,
        "cpu_utilization": cpu_utilization,
        "throughput": throughput,
        "context_switches": context_switches,
        "gantt_chart": gantt_chart
    }
