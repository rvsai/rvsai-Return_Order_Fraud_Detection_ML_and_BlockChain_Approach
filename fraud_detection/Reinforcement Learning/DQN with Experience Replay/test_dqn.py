import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained DQN model
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

# Load the model with custom objects specified
dqn_model = load_model('dqn_model_immediate_feedback.h5', custom_objects={'mse': MeanSquaredError()})

# Load the preprocessed test data
data = pd.read_csv('./data/X_test.csv')  # Assuming 'OrderID' is one of the columns
y_test = pd.read_csv('./data/y_test.csv').values.flatten()  # Convert to 1D array if necessary

# Exclude 'OrderID' and 'RefundIssued' if they are still in the dataset
X_test = data.drop(columns=['OrderID', 'RefundIssued']).values

# Make predictions
y_pred_probs = dqn_model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)  # Get the predicted classes (0 or 1 for non-fraud or fraud)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print evaluation metrics
print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)

# Visualization of the confusion matrix
#plt.figure(figsize=(8, 6))
#sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Fraud', 'Fraud'], yticklabels=['Non-Fraud', 'Fraud'])
##plt.xlabel('Predicted')
#plt.ylabel('Actual')
#plt.title('Confusion Matrix')
#plt.show()

# Visualize prediction probabilities (optional)
#plt.figure(figsize=(10, 6))
#plt.hist(y_pred_probs[:, 1], bins=20, alpha=0.7, label='Predicted Fraud Probability')
#plt.xlabel('Probability')
#plt.ylabel('Frequency')
#plt.title('Distribution of Predicted Fraud Probabilities')
#plt.legend()
#plt.show()
