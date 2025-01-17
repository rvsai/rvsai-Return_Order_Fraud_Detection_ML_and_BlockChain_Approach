import pandas as pd
import json
import random

# Load the dataset
dataset = pd.read_csv("Fraud_return_Orders_ds.csv")  # Replace with your dataset filename

# Ensure the dataset has the required 'Fraud' column
if "Fraud" not in dataset.columns:
    raise ValueError("The dataset must contain a 'Fraud' column to determine customer scores.")

# Define function to generate customerScore
def generate_customer_score(fraud_label):
    if fraud_label == 0:  # Non-Fraud
        return random.randint(71, 100)  # High score for non-fraud
    elif fraud_label == 1:  # Fraud
        return random.randint(0, 70)  # Low score for fraud

# Add 'customerScore' column based on 'Fraud'
dataset["customerScore"] = dataset["Fraud"].apply(generate_customer_score)

# Rename columns to match the exact keys required for JSON
dataset.rename(columns={
    "OrderID": "orderID",
    "ProductCategory": "productCategory",
    "QuantityReturned": "quantityReturned",
    "PurchaseAmount": "purchaseAmount",
    "RefundIssued": "refundIssued",
    "CustomerAccountAge": "customerAccountAge",
    "PreviousReturns": "previousReturns",
    "PreviousFraudReports": "previousFraudReports",
    "DeliveryType": "deliveryType",
    "ReturnCondition": "returnCondition",
}, inplace=True)

# Convert to JSON format
transactions = dataset.to_dict(orient="records")

# Save as JSON file
with open("test_transactions.json", "w") as json_file:
    json.dump(transactions, json_file, indent=4)

print(f"Converted {len(transactions)} transactions to JSON.")
