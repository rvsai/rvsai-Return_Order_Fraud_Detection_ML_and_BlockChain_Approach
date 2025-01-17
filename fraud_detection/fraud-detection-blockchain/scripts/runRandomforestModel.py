from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model
model_pipeline = joblib.load('random_forest_fraud_model.pkl')  # The pipeline includes the model

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from POST request
        data = request.get_json(force=True)
        
        # Ensure the input contains all required features
        required_features = [
            'QuantityReturned',
            'PurchaseAmount',
            'CustomerAccountAge',
            'PreviousReturns',
            'PreviousFraudReports',
            'RefundIssued',
            'ProductCategory',
            'ReasonForReturn',
            'DeliveryType',
            'ReturnCondition'
        ]

        # Verify if all required features are present
        for feature in required_features:
            if feature not in data:
                return jsonify({'error': f'Missing required feature: {feature}'}), 400

        # Convert input data into a DataFrame
        df_input = pd.DataFrame([data])

        # Make prediction using the model pipeline
        prediction = model_pipeline.predict(df_input)

        # Return the result as JSON
        result = {
            'prediction': 'Fraud' if prediction[0] == 1 else 'Not Fraud',
            'input_data': data  # Include input data in the response for reference
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
