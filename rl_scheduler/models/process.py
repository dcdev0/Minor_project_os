class Process:

    def __init__(
        self,
        pid,
        arrival_time,
        burst_time,
        cpu_request,
        memory_request,
        priority
    ):

        self.pid = pid

        self.arrival_time = arrival_time

        self.burst_time = burst_time

        self.remaining_time = burst_time

        self.cpu_request = cpu_request

        self.memory_request = memory_request

        self.priority = priority

        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
