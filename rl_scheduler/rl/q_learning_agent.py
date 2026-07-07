import numpy as np
import random


class QLearningAgent:
    """
    Tabular Q-Learning Agent
    """

    def __init__(
        self,
        state_bins=(5, 5, 5, 5),
        num_actions=6,
        alpha=0.1,
        gamma=0.95,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    ):

        self.alpha = alpha

        self.gamma = gamma

        self.epsilon = epsilon

        self.epsilon_decay = epsilon_decay

        self.epsilon_min = epsilon_min

        self.num_actions = num_actions

        self.q_table = np.zeros(
            state_bins + (num_actions,)
        )

    # ----------------------------------------
    # Action Selection
    # ----------------------------------------

    def choose_action(
        self,
        state
    ):

        if random.random() < self.epsilon:

            return random.randint(
                0,
                self.num_actions - 1
            )

        return int(
            np.argmax(
                self.q_table[state]
            )
        )

    # ----------------------------------------
    # Learning
    # ----------------------------------------

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        current_q = self.q_table[
            state + (action,)
        ]

        best_next = np.max(
            self.q_table[next_state]
        )

        target = reward + self.gamma * best_next

        self.q_table[
            state + (action,)
        ] += self.alpha * (
            target - current_q
        )

    # ----------------------------------------
    # Terminal Update
    # ----------------------------------------

    def update_terminal(
        self,
        state,
        action,
        reward
    ):
        """
        Q-learning update for terminal episodes.
        """

        current_q = self.q_table[
            state + (action,)
        ]

        self.q_table[
            state + (action,)
        ] += self.alpha * (
            reward - current_q
        )
    # ----------------------------------------
    # Exploration Decay
    # ----------------------------------------

    def decay_epsilon(self):

        self.epsilon = max(

            self.epsilon_min,

            self.epsilon *
            self.epsilon_decay

        )

    # ----------------------------------------
    # Helpers
    # ----------------------------------------

    def get_q_table(self):

        return self.q_table

    def save(
        self,
        path
    ):

        np.save(
            path,
            self.q_table
        )

    def load(
        self,
        path
    ):

        self.q_table = np.load(
            path
        )
