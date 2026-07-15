import os
import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, save_dir="plots"):
        """
        Create the directory where all plots will be saved.
        """
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def _save_plot(self, filename):
        """
        Save the current figure to the plots directory.
        """
        plt.savefig(
            os.path.join(self.save_dir, filename),
            dpi=300,
            bbox_inches="tight"
        )

    def plot_training(self, history):

        # Reward
        plt.figure(figsize=(8, 5))
        plt.plot(history["rewards"])
        plt.title("Reward vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Selected Quantum
        plt.figure(figsize=(8, 5))
        plt.plot(history["selected_quantums"])
        plt.title("Selected Quantum vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Quantum")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Waiting Time
        plt.figure(figsize=(8, 5))
        plt.plot(history["episode_waiting"])
        plt.title("Waiting Time vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Waiting Time")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Response Time
        plt.figure(figsize=(8, 5))
        plt.plot(history["episode_response"])
        plt.title("Response Time vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Response Time")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Throughput
        plt.figure(figsize=(8, 5))
        plt.plot(history["episode_throughput"])
        plt.title("Throughput vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Throughput")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Context Switches
        plt.figure(figsize=(8, 5))
        plt.plot(history["episode_context"])
        plt.title("Context Switches vs Episode")
        plt.xlabel("Episode")
        plt.ylabel("Context Switches")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_comparison(self, results):

        schedulers = list(results.keys())

        waiting = [
            results[x]["avg_waiting_time"]
            for x in schedulers
        ]

        turnaround = [
            results[x]["avg_turnaround_time"]
            for x in schedulers
        ]

        response = [
            results[x]["avg_response_time"]
            for x in schedulers
        ]

        throughput = [
            results[x]["throughput"]
            for x in schedulers
        ]

        context = [
            results[x]["context_switches"]
            for x in schedulers
        ]

        metrics = [

            ("Average Waiting Time", waiting),

            ("Average Turnaround Time", turnaround),

            ("Average Response Time", response),

            ("Throughput", throughput),

            ("Context Switches", context)

        ]

        for title, values in metrics:

            plt.figure(figsize=(8, 5))

            plt.bar(schedulers, values)

            plt.title(title)

            plt.xlabel("Scheduler")

            plt.ylabel(title)

            plt.xticks(rotation=45)

            plt.grid(axis="y", linestyle="--", alpha=0.5)

            plt.tight_layout()

            filename = (
                title.lower()
                .replace(" ", "_")
                .replace("/", "_")
                + ".png"
            )

            self._save_plot(filename)

            plt.show()

        # RL Quantum Distribution
        plt.figure(figsize=(8, 5))

        plt.hist(
            results["RL"]["selected_quantums"],
            bins=len(set(results["RL"]["selected_quantums"])),
            rwidth=0.8
        )

        plt.title("RL Selected Quantum Distribution")

        plt.xlabel("Quantum")

        plt.ylabel("Frequency")

        plt.grid(True)

        plt.tight_layout()

        self._save_plot("rl_selected_quantum_distribution.png")

        plt.show()
