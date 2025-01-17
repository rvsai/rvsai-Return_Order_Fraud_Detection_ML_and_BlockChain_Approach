import numpy as np

class FraudEnvironment:
    def __init__(self, features, targets):
        self.features = features
        self.targets = targets
        self.current_index = 0

    def reset(self):
        """Resets the environment to the initial state."""
        self.current_index = np.random.choice(len(self.features))
        return self.features[self.current_index]

    def step(self, action):
        """Takes an action and transitions to the next state."""
        reward = self._calculate_reward(action)
        self.current_index = (self.current_index + 1) % len(self.features)
        next_state = self.features[self.current_index] if self.current_index < len(self.features) else None
        done = self.current_index == len(self.features) - 1
        return next_state, reward, done

    def _calculate_reward(self, action):
        """Calculates the reward based on the action taken."""
        target = self.targets[self.current_index]  # Adjust indexing based on type
        return 1 if action == target else -1
