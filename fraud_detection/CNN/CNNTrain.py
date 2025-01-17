import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical

def load_data():
    X_train = pd.read_csv('./data_30F_70NF/X_train.csv').values
    y_train = pd.read_csv('./data_30F_70NF/y_train.csv').values
    X_test = pd.read_csv('./data_30F_70NF/X_test.csv').values
    y_test = pd.read_csv('./data_30F_70NF/y_test.csv').values
    
    # Print the shape of X_train to understand its structure
    print("Shape of X_train before reshaping:", X_train.shape)

    # One-hot encode y_train and y_test if they're not already
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    
    # Reshape X_train and X_test according to the correct feature number
    # Assuming the second dimension is the number of features per sample
    X_train = X_train.reshape((-1, X_train.shape[1], 1))
    X_test = X_test.reshape((-1, X_test.shape[1], 1))
    
    return X_train, y_train, X_test, y_test

from tensorflow.keras.layers import BatchNormalization

def build_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        Conv1D(32, kernel_size=3, activation='relu'),
        BatchNormalization(),
        MaxPooling1D(2),
        Conv1D(64, kernel_size=3, activation='relu'),
        BatchNormalization(),
        MaxPooling1D(2),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.3),  # Adjusted dropout rate
        Dense(2, activation='softmax')
    ])
    return model


def main():
    X_train, y_train, X_test, y_test = load_data()
    
    model = build_model((X_train.shape[1], 1))  # Use dynamic shape based on the data
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Callbacks
    checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_accuracy', mode='max')
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001)
    
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32, callbacks=[checkpoint, reduce_lr])
    model.save('cnn_model_final.h5')
    print("Model training completed and saved.")

if __name__ == "__main__":
    main()
