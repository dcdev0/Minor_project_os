# rl/train.py

from tqdm import tqdm


def train(
    env,
    agent,
    episodes=1000
):

    rewards = []

    quantums = []

    waiting_times = []

    turnaround_times = []

    response_times = []

    throughputs = []

    context_switches = []

    for episode in tqdm(range(episodes)):

        # -----------------------------
        # Initial workload state
        # -----------------------------

        state = env.reset()

        # -----------------------------
        # Choose action
        # -----------------------------

        action = agent.choose_action(
            state
        )

        # -----------------------------
        # Run scheduler
        # -----------------------------

        _, reward, done, info = env.step(
            action
        )

        # -----------------------------
        # Terminal Q-learning update
        # -----------------------------

        agent.update_terminal(
            state,
            action,
            reward
        )

        agent.decay_epsilon()

        rewards.append(reward)

        quantums.append(info["selected_quantum"])

        waiting_times.append(info["avg_waiting_time"])

        turnaround_times.append(info["avg_turnaround_time"])

        response_times.append(info["avg_response_time"])

        throughputs.append(info["throughput"])

        context_switches.append(info["context_switches"])

        if (episode + 1) % 100 == 0:

            avg_reward = sum(
                rewards[-100:]
            ) / 100

            print(
                f"Episode {episode+1}"
                f" | Avg Reward {avg_reward:.3f}"
                f" | ε={agent.epsilon:.3f}"
            )

    return {

        "rewards": rewards,

        "selected_quantums": quantums,

        "episode_waiting": waiting_times,

        "episode_turnaround": turnaround_times,

        "episode_response": response_times,

        "episode_throughput": throughputs,

        "episode_context": context_switches,

        "q_table": agent.get_q_table()
    }
