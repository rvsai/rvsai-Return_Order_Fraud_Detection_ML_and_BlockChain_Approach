from sklearn.utils import resample
import pandas as pd

# Load your dataset
df = pd.read_csv('C:/Users/raval/fraud_detection/data/Fraud_return_Orders_ds.csv')

# Separate majority and minority classes
df_fraud = df[df['Fraud'] == 1]
df_non_fraud = df[df['Fraud'] == 0]

# Option 1: Create Fraud 30% and Non-Fraud 70% dataset

# Downsample non-fraud class
# Downsample non-fraud class (with replacement)
df_non_fraud_downsampled = resample(df_non_fraud,
                                    replace=True,  # Allow replacement
                                    n_samples=len(df_fraud) * 7 // 3,  # Adjust to get 70% Non-Fraud
                                    random_state=42)

# Combine both classes
df_30fraud = pd.concat([df_fraud, df_non_fraud_downsampled])

# Option 2: Create Fraud 70% and Non-Fraud 30% dataset

# Downsample fraud class
df_fraud_downsampled = resample(df_fraud,
                                replace=True, # Sample with replacement
                                n_samples=len(df_non_fraud) * 7 // 3, # Adjust to get 70% Fraud
                                random_state=42)

# Combine both classes
df_70fraud = pd.concat([df_fraud_downsampled, df_non_fraud])

# Save both modified datasets
df_30fraud.to_csv('fraud_30_nonfraud_70.csv', index=False)
df_70fraud.to_csv('fraud_70_nonfraud_30.csv', index=False)
