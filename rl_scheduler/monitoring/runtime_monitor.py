# monitoring/runtime_monitor.py


class RuntimeMonitor:
    """
    Converts scheduler metrics into a discrete RL state.
    """

    def __init__(self):

        # Bucket thresholds
        self.queue_thresholds = [10, 25, 50, 100]
        self.wait_thresholds = [500, 2000, 5000, 10000]
        self.response_thresholds = [200, 1000, 3000, 6000]
        self.cpu_thresholds = [40, 60, 80, 95]
        self.context_thresholds = [500, 1000, 2000, 4000]

    def bucketize(self, value, thresholds):
        """
        Convert a continuous value into a discrete bucket.
        """

        for i, threshold in enumerate(thresholds):
            if value <= threshold:
                return i

        return len(thresholds)

    def extract_state(self, results):
        """
        Convert scheduler results into a discrete RL state.
        """

        queue_bucket = self.bucketize(
            results["avg_queue_length"],
            self.queue_thresholds
        )

        waiting_bucket = self.bucketize(
            results["avg_waiting_time"],
            self.wait_thresholds
        )

        response_bucket = self.bucketize(
            results["avg_response_time"],
            self.response_thresholds
        )

        cpu_bucket = self.bucketize(
            results["runtime_cpu_utilization"],
            self.cpu_thresholds
        )

        context_bucket = self.bucketize(
            results["context_switches"],
            self.context_thresholds
        )

        return (
            queue_bucket,
            waiting_bucket,
            response_bucket,
            cpu_bucket,
            context_bucket
        )
