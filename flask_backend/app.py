import pandas as pd
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Load the trained Pipeline
# This pipeline already contains the scaler and the model
try:
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Success: Model pipeline loaded!")
except FileNotFoundError:
    print("Error: model/model.pkl not found. Make sure you moved it to the 'model' folder.")
    model = None

@app.route('/')
def home():
    return "Cardio Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model is not loaded'}), 500
    
    data = request.get_json()
    
    # 2. Extract features from the JSON request
    # We expect the frontend to send these raw values
    try:
        features = {
            'age': data['age'],          # In years
            'gender': data['gender'],    # 1 or 0 (as processed in your notebook)
            'height': data['height'],    # In cm
            'weight': data['weight'],    # In kg
            'ap_hi': data['ap_hi'],      # Systolic BP
            'ap_lo': data['ap_lo'],      # Diastolic BP
            'cholesterol': data['cholesterol'], # 1, 2, or 3
            'gluc': data['gluc'],        # 1, 2, or 3
            'smoke': data['smoke'],      # 0 or 1
            'alco': data['alco'],        # 0 or 1
            'active': data['active']     # 0 or 1
        }
        
        # 3. Calculate BMI (Feature Engineering)
        # Your model expects 'bmi' as a feature, so we calculate it here
        # BMI = weight(kg) / (height(m))^2
        height_m = features['height'] / 100
        features['bmi'] = features['weight'] / (height_m ** 2)

        # 4. Create a DataFrame
        # The pipeline REQUIRES a DataFrame with specific column names
        df = pd.DataFrame([features])
        
        # Ensure columns are in the exact order the pipeline expects (optional but safe)
        # Based on your notebook:
        expected_cols = ['height', 'weight', 'age', 'ap_hi', 'ap_lo', 'bmi', 
                         'cholesterol', 'gluc', 'gender', 'smoke', 'alco', 'active']
        df = df[expected_cols]

        # 5. Make Prediction
        prediction = model.predict(df)
        probability = model.predict_proba(df).max() # Get confidence score
        
        # 6. Return Result
        result = int(prediction[0]) # 0 = No Disease, 1 = Disease present
        
        return jsonify({
            'prediction': result,
            'probability': float(probability),
            'message': 'High risk of cardiovascular disease' if result == 1 else 'Low risk',
            'status': 'success'
        })

    except KeyError as e:
        return jsonify({'error': f'Missing required feature: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)