import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Open log file
log_file = open("training_log_main.txt", "w")

# Load preprocessed dataset
df_train = pd.read_csv('./data/X_train.csv')
y_train = pd.read_csv('./data/y_train.csv').values.flatten()  # Load targets from y_train.csv

# Exclude 'OrderID' and 'RefundIssued' if they are still in the dataset
X_train = df_train.drop(columns=['OrderID', 'RefundIssued']).values

# Define a simple DQN model for binary classification
def build_dqn_model(input_shape):
    model = Sequential([
        Dense(64, input_shape=(input_shape,), activation='relu'),
        Dense(32, activation='relu'),
        Dense(2, activation='linear')  # Output layer for two actions: 0 (non-fraud), 1 (fraud)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

input_shape = X_train.shape[1]
dqn_model = build_dqn_model(input_shape)

# Hyperparameters
num_episodes = 50
epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.999
gamma = 0.95

# Training loop
for episode in range(num_episodes):
    state = X_train[np.random.choice(X_train.shape[0])]
    total_reward = 0
    log_file.write(f"Episode {episode+1}\n")
    log_file.write(f"Data Size {len(X_train)}\n")
    for idx in range(len(X_train)):
        q_values = np.zeros(2)  # Initialize q_values to zero for each step
        if np.random.rand() <= epsilon:
            action = np.random.choice([0, 1])
        else:
            q_values = dqn_model.predict(state.reshape(1, -1)).flatten()
            action = np.argmax(q_values)

        true_label = y_train[idx]
        reward = 1 if action == true_label else -1

        if idx + 1 < len(X_train):
            next_state = X_train[idx + 1]
            q_values_next = dqn_model.predict(next_state.reshape(1, -1)).flatten()
            target = reward + gamma * np.max(q_values_next)
            q_values[action] = target
            dqn_model.fit(state.reshape(1, -1), q_values.reshape(1, -1), epochs=1, verbose=0)

        state = X_train[idx]
        total_reward += reward
      

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
    
    log_file.write(f"Episode {episode+1}, Total Reward: {total_reward}\n")
    log_file.flush()  # Ensure logs are written immediately

dqn_model.save('dqn_model_immediate_feedback.h5')
log_file.write("Training completed.\n")
log_file.close()
print("Training completed.")