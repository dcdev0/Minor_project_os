import matplotlib.pyplot as plt


class Plotter:

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

        # Quantum
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

            plt.xticks(rotation=45)

            plt.tight_layout()

            plt.show()

        plt.figure(figsize=(8, 5))

        plt.hist(
            results["RL"]["selected_quantums"],
            bins=[2, 4, 6, 8, 12, 16, 18],
            rwidth=0.8
        )

        plt.title("RL Selected Quantum Distribution")

        plt.xlabel("Quantum")

        plt.ylabel("Frequency")

        plt.grid(True)

        plt.show()
