# environment/scheduler_env.py

from loaders.google_trace_loader import TraceDataset
from schedulers.rr_core import run_rr
from monitoring.runtime_monitor import RuntimeMonitor


class SchedulerEnv:
    """
    Reinforcement Learning Environment
    for Adaptive Round Robin Scheduling.
    """

    # -----------------------------
    # Action Space
    # -----------------------------

    ACTIONS = [4, 6, 8, 10, 12, 14, 16]

    def __init__(self, dataset, window_size=1000):

        self.dataset = dataset

        self.window_size = window_size

        self.monitor = RuntimeMonitor()

        # -----------------------------------
        # Reward Normalization Statistics
        # -----------------------------------

        self.reward_stats = {

            "waiting_min": float("inf"),
            "waiting_max": float("-inf"),

            "response_min": float("inf"),
            "response_max": float("-inf"),

            "context_min": float("inf"),
            "context_max": float("-inf"),

            "throughput_min": float("inf"),
            "throughput_max": float("-inf")
        }

        # -----------------------------------
    # Discretize Workload State
    # -----------------------------------

    def discretize_state(self, features):
        """
        Convert workload features into a discrete state.
        """

        def bucket(value, thresholds):

            for i, t in enumerate(thresholds):

                if value <= t:
                    return i

            return len(thresholds)

        avg_burst_bucket = bucket(
            features["avg_burst"],
            [20, 50, 100, 200]
        )

        burst_std_bucket = bucket(
            features["burst_std"],
            [10, 30, 60, 100]
        )

        short_ratio_bucket = bucket(
            features["short_ratio"],
            [0.2, 0.4, 0.6, 0.8]
        )

        long_ratio_bucket = bucket(
            features["long_ratio"],
            [0.1, 0.3, 0.5, 0.7]
        )

        return (
            avg_burst_bucket,

            burst_std_bucket,

            short_ratio_bucket,

            long_ratio_bucket

        )

    # -----------------------------------
    # Reset
    # -----------------------------------

    def reset(self):
        """
        Start a new episode.

        Returns
        -------
        state
        """

        self.processes = self.dataset.sample_window(self.window_size)

        features = self.dataset.workload_features(self.processes)

        state = self.discretize_state(features)

        return state

    # -----------------------------------
    # Step
    # -----------------------------------

    def step(
            self,
            action
    ):
        """
        Parameters
        ----------
        action : int

        Returns
        -------
        next_state,
        reward,
        done,
        info
        """

        quantum = self.ACTIONS[action]

        results = run_rr(

            self.processes,

            quantum=quantum

        )

        next_state = self.monitor.extract_state(
            results
        )

        reward = self.compute_reward(
            results
        )

        results["reward"] = reward

        results["selected_quantum"] = quantum

        done = True

        return (

            None,

            reward,

            done,

            results

        )
        # -----------------------------------
    # Reward
    # -----------------------------------

    def compute_reward(self, results):

        waiting = self.normalize_metric(
            results["avg_waiting_time"],
            "waiting"
        )

        response = self.normalize_metric(
            results["avg_response_time"],
            "response"
        )

        context = self.normalize_metric(
            results["context_switches"],
            "context"
        )

        throughput = self.normalize_metric(
            results["throughput"],
            "throughput"
        )

        reward = (-0.35 * waiting - 0.25 * response -
                  0.20 * context + 0.20 * throughput)

        return reward

    # -----------------------------------
    # Helpers
    # -----------------------------------

    def num_actions(self):

        return len(
            self.ACTIONS
        )

    def action_to_quantum(
            self,
            action
    ):

        return self.ACTIONS[action]

    def normalize_metric(self, value, metric):
        """
        Min-Max normalization using observed values.
        """

        min_key = metric + "_min"
        max_key = metric + "_max"

        self.reward_stats[min_key] = min(
            self.reward_stats[min_key],
            value
        )

        self.reward_stats[max_key] = max(
            self.reward_stats[max_key],
            value
        )

        minimum = self.reward_stats[min_key]
        maximum = self.reward_stats[max_key]

        if maximum == minimum:
            return 0.5

        return (value - minimum) / (maximum - minimum)
