import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load dataset
df = pd.read_csv('./data/encodedDataset.csv')  # Ensure you have the correct path

# Select columns to scale
features_to_standard_scale = ['QuantityReturned', 'PurchaseAmount', 'CustomerAccountAge']
features_to_minmax_scale = ['PreviousReturns', 'PreviousFraudReports']

# Apply Standard Scaler
standard_scaler = StandardScaler()
df[features_to_standard_scale] = standard_scaler.fit_transform(df[features_to_standard_scale])

# Apply Min-Max Scaler
minmax_scaler = MinMaxScaler()
df[features_to_minmax_scale] = minmax_scaler.fit_transform(df[features_to_minmax_scale])

# Split the dataset into train and test sets
X = df.drop('Fraud', axis=1)
y = df['Fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Save the datasets
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("Training and testing datasets have been saved to separate CSV files.")
