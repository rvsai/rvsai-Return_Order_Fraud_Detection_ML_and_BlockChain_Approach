import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_and_save_dataset(input_file, output_file):
    data = pd.read_csv(input_file)
    categorical_features = ['ProductCategory', 'ReasonForReturn', 'ReturnCondition', 'DeliveryType']
    target_variable = 'Fraud'  # Assuming 'Fraud' is the target variable
    numerical_features = data.drop(columns=categorical_features + [target_variable])

    # Initializing the OneHotEncoder
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(data[categorical_features]).toarray()

    # Getting the feature names from encoder
    feature_names = encoder.get_feature_names_out(categorical_features)
    
    # Create DataFrame for encoded features
    encoded_features_df = pd.DataFrame(encoded_features, columns=feature_names)
    
    # Combine all features with the target variable
    final_df = pd.concat([numerical_features, encoded_features_df, data[target_variable]], axis=1)
    
    try:
        final_df.to_csv(output_file, index=False)
        print("Data saved to", output_file)
    except Exception as e:
        print("Error saving data:", str(e))

# Specify the input and output file paths
input_file = './data/Fraud_return_Orders_ds.csv'
output_file = './data/encodedDataset.csv'

# Call the function
encode_and_save_dataset(input_file, output_file)
