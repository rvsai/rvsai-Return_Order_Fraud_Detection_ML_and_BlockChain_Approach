import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed training data
X_train = pd.read_csv('./data_70F_30NF/X_train.csv').values  # Convert to numpy array if not already
y_train = pd.read_csv('./data_70F_30NF/y_train.csv').values.flatten()  # Convert to 1D array if necessary

# Initialize the AdaBoost classifier with a base Decision Tree
base_estimator = DecisionTreeClassifier(max_depth=1)
adaboost_model = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=42)  # Use 'estimator' instead of 'base_estimator'

# Train the AdaBoost classifier
adaboost_model.fit(X_train, y_train)
print("Training completed.")

# Save the trained model (optional, using joblib for saving)
import joblib
joblib.dump(adaboost_model, 'adaboost_model.joblib')
