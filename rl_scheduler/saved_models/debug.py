import numpy as np

q = np.load("q_table.npy")

print("Learned Policy\n")

for index in np.ndindex(q.shape[:-1]):

    values = q[index]

    if np.any(values != 0):

        action = np.argmax(values)

        print(
            f"State {index} "
            f"-> Action {action} "
            f"(Quantum {[2, 4, 6, 8, 12, 16][action]}) "
            f"Q={values[action]:.4f}"
        )
