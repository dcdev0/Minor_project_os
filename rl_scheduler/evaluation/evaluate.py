import copy

from schedulers.rr_core import run_rr


class Evaluator:
    """
    Fair comparison between baseline Round Robin
    and RL-assisted Round Robin.

    Every scheduler is evaluated on the SAME
    workload window.
    """

    BASELINE_QUANTUMS = [2, 4, 6, 8, 12, 16]

    def __init__(self, dataset, env, agent):

        self.dataset = dataset
        self.env = env
        self.agent = agent

    # -------------------------------------------------

    def evaluate(
        self,
        num_windows=50,
        window_size=1000
    ):

        results = {}

        # ---------------------------------------
        # initialize result storage
        # ---------------------------------------

        for q in self.BASELINE_QUANTUMS:

            results[f"RR_Q{q}"] = {

                "avg_waiting_time": [],
                "avg_turnaround_time": [],
                "avg_response_time": [],
                "throughput": [],
                "context_switches": []

            }

        results["RL"] = {

            "avg_waiting_time": [],
            "avg_turnaround_time": [],
            "avg_response_time": [],
            "throughput": [],
            "context_switches": [],
            "selected_quantums": []

        }

        # ---------------------------------------
        # Evaluate each workload window
        # ---------------------------------------

        old_eps = self.agent.epsilon
        self.agent.epsilon = 0.0

        for window in range(num_windows):

            # Sample ONE workload

            workload = self.dataset.sample_window(
                window_size
            )

            # ===============================
            # Baseline RR
            # ===============================

            for quantum in self.BASELINE_QUANTUMS:

                metrics = run_rr(

                    copy.deepcopy(workload),

                    quantum=quantum

                )

                scheduler = f"RR_Q{quantum}"

                for key in [

                    "avg_waiting_time",

                    "avg_turnaround_time",

                    "avg_response_time",

                    "throughput",

                    "context_switches"

                ]:

                    results[scheduler][key].append(
                        metrics[key]
                    )

            # ===============================
            # RL Scheduler
            # ===============================

            self.env.processes = copy.deepcopy(
                workload
            )

            features = self.dataset.workload_features(
                self.env.processes
            )

            state = self.env.discretize_state(
                features
            )

            action = self.agent.choose_action(
                state
            )

            _, _, _, metrics = self.env.step(
                action
            )

            for key in [

                "avg_waiting_time",

                "avg_turnaround_time",

                "avg_response_time",

                "throughput",

                "context_switches"

            ]:

                results["RL"][key].append(
                    metrics[key]
                )

            results["RL"]["selected_quantums"].append(

                metrics["selected_quantum"]

            )

        self.agent.epsilon = old_eps

        # ---------------------------------------
        # Average all metrics
        # ---------------------------------------

        final_results = {}

        for scheduler in results:

            final_results[scheduler] = {}

            for metric, values in results[scheduler].items():

                if metric == "selected_quantums":

                    final_results[scheduler][metric] = values

                else:

                    final_results[scheduler][metric] = (

                        sum(values) / len(values)

                    )

        return final_results
