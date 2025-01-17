import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

# Load preprocessed dataset
df_train = pd.read_csv('./data/X_train.csv')
y_train = pd.read_csv('./data/y_train.csv').values.flatten()  # Load targets from y_train.csv

# Exclude 'OrderID' and 'RefundIssued' if they are still in the dataset
X_train = df_train.drop(columns=['OrderID', 'RefundIssued']).values

def build_dqn_model(input_shape):
    model = Sequential([
        Input(shape=(input_shape,)),
        Dense(256, activation='relu'),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(2, activation='linear')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# Path for the model checkpoint
checkpoint_path = 'checkpoints/model_weights_epoch_{epoch:02d}.keras'  # Use .keras for the model format

# Load or build the model
try:
    dqn_model = load_model('dqn_model_immediate_feedback.h5')
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    input_shape = X_train.shape[1]
    dqn_model = build_dqn_model(input_shape)
    print("New model built.")

# ModelCheckpoint callback to save the model at each epoch end
checkpoint = ModelCheckpoint(filepath=checkpoint_path, monitor='loss', verbose=1, save_best_only=True, mode='min', save_weights_only=False)

# Hyperparameters
num_episodes = 50
batch_size = 32
epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.990
gamma = 0.95

# Training loop
for episode in range(num_episodes):
    total_reward = 0
    batch_states = []
    batch_targets = []
    print(f"Starting Episode {episode + 1}")

    for idx in range(len(X_train)):
        state = X_train[np.random.choice(X_train.shape[0])]
        q_values = np.zeros(2)

        if np.random.rand() <= epsilon:
            action = np.random.choice([0, 1])
        else:
            q_values = dqn_model.predict(state.reshape(1, -1)).flatten()
            action = np.argmax(q_values)

        true_label = y_train[idx]
        reward = 1 if action == true_label else -1
        total_reward += reward

        next_state = X_train[(idx + 1) % len(X_train)]
        q_values_next = dqn_model.predict(next_state.reshape(1, -1)).flatten()
        target = q_values.copy()
        target[action] = reward + gamma * np.max(q_values_next)

        batch_states.append(state)
        batch_targets.append(target)

        # Batch update
        if len(batch_states) >= batch_size or idx == len(X_train) - 1:
            dqn_model.fit(np.array(batch_states), np.array(batch_targets), batch_size=len(batch_states), verbose=0, callbacks=[checkpoint])
            batch_states, batch_targets = [], []

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

    print(f"Total Reward for Episode {episode+1}: {total_reward}")

dqn_model.save('dqn_model_immediate_feedback.h5')
print("Training completed.")
