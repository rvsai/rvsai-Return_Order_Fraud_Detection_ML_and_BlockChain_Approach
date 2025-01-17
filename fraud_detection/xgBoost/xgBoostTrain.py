import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load your preprocessed dataset
X_train = pd.read_csv('./data_70F_30NF/X_train.csv').values  # Features dataset
y_train = pd.read_csv('./data_70F_30NF/y_train.csv').values.flatten()  # Fraud/Non-Fraud labels



# Calculate scale_pos_weight
num_negative = sum(y_train == 0)
num_positive = sum(y_train == 1)
scale_pos_weight = num_negative / num_positive

# Initialize the model with scale_pos_weight
xgb_model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, 
                          scale_pos_weight=scale_pos_weight, random_state=42)

# Train the model
xgb_model.fit(X_train, y_train)



# Save the trained model
xgb_model.save_model('xgb_model.json')

print("XGBoost Model Training Completed.")
