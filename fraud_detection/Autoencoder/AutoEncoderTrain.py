import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error

def load_data():
    # Load your data
    X_train = pd.read_csv('./data/X_train.csv').values
    X_test = pd.read_csv('./data/X_test.csv').values
    return X_train, X_test

def build_autoencoder(input_dim):
    input_layer = Input(shape=(input_dim,))
    # Encoder
    encoded = Dense(128, activation='relu')(input_layer)
    encoded = Dense(64, activation='relu')(encoded)
    encoded = Dense(32, activation='relu')(encoded)  # Latent space representation

    # Decoder
    decoded = Dense(64, activation='relu')(encoded)
    decoded = Dense(128, activation='relu')(decoded)
    decoded = Dense(input_dim, activation='sigmoid')(decoded)  # Reconstruction

    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')
    return autoencoder

def train_autoencoder(autoencoder, X_train):
    autoencoder.fit(X_train, X_train, epochs=50, batch_size=256, shuffle=True, validation_split=0.2)

def evaluate_autoencoder(autoencoder, X_test):
    # Predict the reconstruction from the test set
    predicted = autoencoder.predict(X_test)
    mse = np.mean(np.power(X_test - predicted, 2), axis=1)
    print("Reconstruction error (MSE) on Test Set:", mse)

def main():
    X_train, X_test = load_data()
    autoencoder = build_autoencoder(X_train.shape[1])
    train_autoencoder(autoencoder, X_train)
    evaluate_autoencoder(autoencoder, X_test)
    autoencoder.save('autoencoder_model.h5')
    print("Autoencoder training completed and saved.")

if __name__ == "__main__":
    main()
