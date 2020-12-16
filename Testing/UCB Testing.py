# import modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class ucb_bandit:
    '''
    Upper Confidence Bound Bandit

    Inputs
    ============================================
    k: number of arms (int)
    c:
    iters: number of steps (int)
    mu: set the average rewards for each of the k-arms.
        Set to "random" for the rewards to be selected from
        a normal distribution with mean = 0.
        Set to "sequence" for the means to be ordered from
        0 to k-1.
        Pass a list or array of length = k for user-defined
        values.
    '''

    def __init__(self, k, c, iters, mu='Pilot_Priors'):
        # Number of arms
        self.k = 4
        # Exploration parameter
        self.c = 0.5
        # Number of iterations
        self.iters = 150
        # Step count
        self.n = 1
        # Step count for each arm
        self.k_n = np.ones(k)
        # Total mean reward
        self.mean_reward = 0
        self.reward = np.zeros(iters)
        # Mean reward for each arm
        self.k_reward = np.zeros(k)

        if type(mu) == list or type(mu).__module__ == np.__name__ or mu == 'Pilot_Priors':
            # User-defined averages
            urn1 = [-4, -3, 4, 12]
            urn2 = [-4, -3, 4, 12]
            urn3 = [-7, -6, 1, 9]
            urn4 = [2, 2, 2, 2]

            draw1 = np.random.choice(urn1, 1, p=[0.125, 0.125, 0.39063, 0.35937])
            draw2 = np.random.choice(urn2, 1, p=[0.35937, 0.39063, 0.125, 0.125])
            draw3 = np.random.choice(urn3, 1, p=[0.125, 0.125, 0.39063, 0.35937])
            draw4 = 2

            draw11 = int(draw1)
            draw22 = int(draw2)
            draw33 = int(draw3)

            liste = [draw11, draw22, draw33, draw4]
            self.mu = np.array(liste)

        elif mu == 'random':
            # Draw means from probability distribution
            self.mu = np.random.normal(0, 1, k)
        elif mu == 'sequence':
            # Increase the mean for each arm by one
            self.mu = np.linspace(0, k - 1, k)

    def pull(self):
        # Select action according to UCB Criteria
        a = np.argmax(self.k_reward + self.c * np.sqrt(
            (np.log(self.n)) / self.k_n))

        print(a)
        reward = self.mu[a]
        print(reward)
        # Update counts
        self.n += 1
        self.k_n[a] += 1

        # Update total
        self.mean_reward = self.mean_reward + (
                reward - self.mean_reward) / self.n

        # Update results for a_k
        self.k_reward[a] = self.k_reward[a] + (
                reward - self.k_reward[a]) / self.k_n[a]

    def run(self):
        for i in range(self.iters):
            self.pull()
            self.reward[i] = self.mean_reward

    def reset(self, mu=None):
        # Resets results while keeping settings
        self.n = 1
        self.k_n = np.ones(self.k)
        self.mean_reward = 0
        self.reward = np.zeros(iters)
        self.k_reward = np.zeros(self.k)
        if mu == 'Pilot_Priors':
            urn1 = [-4, -3, 4, 12]
            urn2 = [-4, -3, 4, 12]
            urn3 = [-7, -6, 1, 9]
            urn4 = [2, 2, 2, 2]

            draw1 = np.random.choice(urn1, 1, p=[0.125, 0.125, 0.39063, 0.35937])
            draw2 = np.random.choice(urn2, 1, p=[0.35937, 0.39063, 0.125, 0.125])
            draw3 = np.random.choice(urn3, 1, p=[0.125, 0.125, 0.39063, 0.35937])
            draw4 = 2

            draw11 = int(draw1)
            draw22 = int(draw2)
            draw33 = int(draw3)

            liste = [draw11, draw22, draw33, draw4]
            self.mu = np.array(liste)


iters = 150
k = 4

ucb_rewards = np.zeros(iters)
# Initialize bandits
ucb = ucb_bandit(k, 2, iters)
episodes = 10000
# Run experiments
for i in range(episodes):
    ucb.reset('Pilot_Priors')
    # Run experiments
    ucb.run()

    # Update long-term averages
    ucb_rewards = ucb_rewards + (
            ucb.reward - ucb_rewards) / (i + 1)


plt.figure(figsize=(12,8))
plt.plot(ucb_rewards, label="UCB")
plt.legend(bbox_to_anchor=(1.2, 0.5))
plt.xlabel("Iterations")
plt.ylabel("Average Reward")
plt.title("Average UCB Rewards after "
          + str(episodes) + " Episodes")
plt.show()

