from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('E:/f1/f1_rf_model (1).pkl')
except FileNotFoundError:
    print("Error: Model file 'f1_rf_model.pkl' not found.")
    raise

# Define features for prediction
FEATURES = ['grid', 'position_qualifying', 'avg_driver_points', 'avg_constructor_points',
            'avg_lap_time_ms', 'fastestLapTime_seconds']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        input_data = []
        for feature in FEATURES:
            value = request.form.get(feature)
            if not value:
                return jsonify({'error': f'Missing value for {feature}'}), 400
            try:
                input_data.append(float(value))
            except ValueError:
                return jsonify({'error': f'Invalid input for {feature}. Must be a number.'}), 400

        # Prepare input for model
        input_array = np.array([input_data])

        # Make prediction (probability of winning)
        prob = model.predict_proba(input_array)[0][1]  # Probability of class 1 (win)
        prediction = f"{prob * 100:.2f}% chance of winning"

        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)