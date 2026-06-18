# dataset_generator.py

import random


class Process:

    def __init__(self, pid, arrival_time, burst_time):

        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        self.remaining_time = burst_time

        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1


# =========================================================
# WORKLOAD GENERATOR
# =========================================================

def generate_dataset(
        num_processes=200,
        workload_type="mixed"
):

    processes = []

    for i in range(num_processes):

        arrival_time = random.randint(0, 50)

        # ---------------------------------------------
        # WORKLOAD TYPES
        # ---------------------------------------------

        if workload_type == "small":

            burst_time = random.randint(1, 10)

        elif workload_type == "medium":

            burst_time = random.randint(10, 50)

        elif workload_type == "large":

            burst_time = random.randint(50, 200)

        elif workload_type == "mixed":

            category = random.choice(
                ["small", "medium", "large"]
            )

            if category == "small":
                burst_time = random.randint(1, 10)

            elif category == "medium":
                burst_time = random.randint(10, 50)

            else:
                burst_time = random.randint(50, 200)

        else:

            burst_time = random.randint(1, 100)

        process = Process(
            pid=f"P{i+1}",
            arrival_time=arrival_time,
            burst_time=burst_time
        )

        processes.append(process)

    return processes
