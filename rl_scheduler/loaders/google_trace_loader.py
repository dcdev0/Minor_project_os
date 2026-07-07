import csv
import random
import copy

from models.process import Process


class TraceDataset:
    """
    Loads the Google Cluster Trace once and provides
    workload samples for the RL scheduler.
    """

    def __init__(self, filepath):

        self.filepath = filepath

        self.processes = []

        self.seed = None

    # ---------------------------------------------------
    # Random Seed
    # ---------------------------------------------------

    def reset_seed(self, seed):

        self.seed = seed

        random.seed(seed)

    # ---------------------------------------------------
    # Load Entire Dataset
    # ---------------------------------------------------

    def load_once(self):

        self.processes = []

        seen_tasks = set()

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                try:

                    if len(row) < 11:
                        continue

                    timestamp = row[0]

                    job_id = row[2]

                    task_index = row[3]

                    priority = row[8]

                    cpu_request = row[9]

                    memory_request = row[10]

                    if cpu_request == "":
                        continue

                    task_id = f"{job_id}_{task_index}"

                    if task_id in seen_tasks:
                        continue

                    seen_tasks.add(task_id)

                    arrival_time = int(timestamp)

                    cpu_request = float(cpu_request)

                    memory_request = (
                        float(memory_request)
                        if memory_request != ""
                        else 0.0
                    )

                    priority = (
                        int(priority)
                        if priority != ""
                        else 0
                    )

                    # Estimated CPU burst

                    burst_time = max(
                        5,
                        int(cpu_request * 500)
                    )

                    process = Process(
                        pid=task_id,
                        arrival_time=arrival_time,
                        burst_time=burst_time,
                        cpu_request=cpu_request,
                        memory_request=memory_request,
                        priority=priority
                    )

                    self.processes.append(process)

                except Exception:

                    continue

        self.processes.sort(
            key=lambda p: p.arrival_time
        )

        print(
            f"Loaded {len(self.processes)} processes."
        )

    # ---------------------------------------------------
    # Window Sampling
    # ---------------------------------------------------

    def sample_window(
        self,
        size=1000
    ):

        if len(self.processes) == 0:

            raise RuntimeError(
                "Dataset not loaded."
            )

        if size > len(self.processes):

            size = len(self.processes)

        start = random.randint(
            0,
            len(self.processes) - size
        )

        window = copy.deepcopy(

            self.processes[
                start:start + size
            ]

        )

        return self.normalize_arrivals(
            window
        )

    # ---------------------------------------------------
    # Normalize Arrival Times
    # ---------------------------------------------------

    def normalize_arrivals(
        self,
        processes
    ):

        if len(processes) == 0:

            return processes

        min_time = min(

            p.arrival_time

            for p in processes

        )

        for process in processes:

            process.arrival_time -= min_time

        return processes

    # ---------------------------------------------------
    # Dataset Statistics
    # ---------------------------------------------------

    def statistics(self, processes=None):

        if processes is None:
            processes = self.processes

        if len(self.processes) == 0:

            return {}

        cpu = [

            p.cpu_request

            for p in processes

        ]

        memory = [

            p.memory_request

            for p in processes

        ]

        priorities = {}

        for process in processes:

            priorities.setdefault(
                process.priority,
                0
            )

            priorities[
                process.priority
            ] += 1

        return {

            "total_tasks":
                len(processes),

            "arrival_start":
                processes[0].arrival_time,

            "arrival_end":
                processes[-1].arrival_time,

            "avg_cpu_request":
                sum(cpu) / len(cpu),

            "avg_memory_request":
                sum(memory) / len(memory),

            "priority_distribution":
                priorities
        }

        # ---------------------------------------------------
    # Workload Features
    # ---------------------------------------------------

    def workload_features(self, processes):
        """
        Compute workload characteristics for the sampled window.

        These features are observable before scheduling and
        are used as the RL state.
        """

        if len(processes) == 0:
            return {}

        avg_cpu_request = (
            sum(p.cpu_request for p in processes)
            / len(processes)
        )

        avg_memory_request = (
            sum(p.memory_request for p in processes)
            / len(processes)
        )

        avg_priority = (
            sum(p.priority for p in processes)
            / len(processes)
        )

        queue_length = len(processes)

        return {

            "queue_length": queue_length,

            "avg_cpu_request": avg_cpu_request,

            "avg_memory_request": avg_memory_request,

            "avg_priority": avg_priority
        }
