import pandas as pd
import time
import memory_profiler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Step 1: Load the dataset
df = pd.read_csv('C:/Users/raval/fraud_detection/data/fraud_30_nonfraud_70.csv')

# Step 2: Preprocessing - Define features and target variable
X = df.drop(columns=['OrderID', 'Fraud'])  # Exclude 'OrderID' and target variable 'Fraud'
y = df['Fraud']  # Target variable

numeric_features = ['QuantityReturned', 'PurchaseAmount', 'CustomerAccountAge', 'PreviousReturns', 'PreviousFraudReports', 'RefundIssued']
categorical_features = ['ProductCategory', 'ReasonForReturn', 'DeliveryType', 'ReturnCondition']

# Step 3: Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)])

# Step 4: Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Measure computational overhead - Memory and Time
mem_before = memory_profiler.memory_usage()[0]
start_time = time.time()

# Step 6: Build the Logistic Regression pipeline
logreg_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier', LogisticRegression(random_state=42, class_weight='balanced'))])

# Step 7: Train the model
logreg_pipeline.fit(X_train, y_train)

# Measure computational overhead after training
end_time = time.time()
mem_after = memory_profiler.memory_usage()[0]

# Calculate computational overhead
training_time = end_time - start_time
memory_used = mem_after - mem_before

# Step 8: Make predictions on the test set
y_pred = logreg_pipeline.predict(X_test)
y_proba = logreg_pipeline.predict_proba(X_test)[:, 1]  # Probabilities for ROC-AUC

# Step 9: Evaluate the model
classification_rep = classification_report(y_test, y_pred, output_dict=True)
roc_auc = roc_auc_score(y_test, y_proba)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC-AUC Score:", roc_auc)
print("Confusion Matrix:\n", conf_matrix)

# Print computational overhead
print(f"Training Time: {training_time:.2f} seconds")
print(f"Memory Used: {memory_used:.2f} MiB")

# Step 10: Save the model
joblib.dump(logreg_pipeline, 'logistic_regression_fraud_model.pkl')

# Step 11: Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig('confusion_matrix.png')
plt.show()

# Step 12: Plot ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig('roc_curve.png')
plt.show()

# Step 13: Plot Precision, Recall, F1-Score for both classes
metrics = ['precision', 'recall', 'f1-score']
classes = ['0 (Non-Fraud)', '1 (Fraud)']

plt.figure(figsize=(10, 6))
for metric in metrics:
    plt.bar(classes, [classification_rep['0'][metric], classification_rep['1'][metric]], label=metric)

plt.title('Precision, Recall, F1-Score Comparison')
plt.legend()
plt.savefig('metrics_comparison.png')
plt.show()

# Step 14: Plot Accuracy
plt.figure(figsize=(6, 4))
plt.bar(['Accuracy'], [classification_rep['accuracy']])
plt.title('Model Accuracy')
plt.savefig('accuracy.png')
plt.show()

# Step 15: Plot computational overhead (Training Time and Memory Usage)
plt.figure(figsize=(6, 4))

# Bar chart for training time and memory usage
overhead_metrics = ['Training Time (s)', 'Memory Used (MiB)']
overhead_values = [training_time, memory_used]

plt.bar(overhead_metrics, overhead_values, color=['blue', 'green'])
plt.title('Computational Overhead')
plt.savefig('computational_overhead.png')
plt.show()
