from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your-secret-key-here'  # Needed for session management and flash messages

# In-memory user storage (replace with a database in production)
users = {}

# Load your pretrained model
try:
    model = load_model('E:/code parts/front end/best_brain_stroke_model (1).h5')
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

# Image size expected by model
IMG_SIZE = (224, 224)

# Helper function to check if user is logged in
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash('Username already exists.', 'error')
        else:
            users[username] = {'password': generate_password_hash(password)}
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    error = None
    results = []
    if request.method == 'POST':
        files = request.files.getlist('images')  # Get list of files from folder
        if not files or all(file.filename == '' for file in files):
            error = "No files found in the selected folder."
            logger.warning(error)
        else:
            try:
                # Ensure upload folder exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                for file in files:
                    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        # Use secure_filename to sanitize the filename
                        filename = secure_filename(os.path.basename(file.filename))
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        logger.debug(f"Saving file to: {filepath}")
                        file.save(filepath)

                        # Preprocess image
                        logger.debug(f"Preprocessing image: {filename}")
                        img = image.load_img(filepath, target_size=IMG_SIZE)
                        img_array = image.img_to_array(img)
                        img_array = np.expand_dims(img_array, axis=0)
                        img_array = img_array / 255.0

                        # Make prediction
                        logger.debug(f"Making prediction for: {filename}")
                        prediction = model.predict(img_array)
                        prediction_text = "Stroke Detected" if prediction[0][0] > 0.5 else "No Stroke Detected"
                        confidence = prediction[0][0] if prediction_text == "Stroke Detected" else 1.0 - prediction[0][0]

                        results.append({
                            "filename": filename,
                            "prediction": prediction_text,
                            "confidence": confidence,
                            "image_path": filepath
                        })

                        logger.info(f"Prediction successful for {filename}: {prediction_text}")
                    else:
                        logger.warning(f"Invalid file format: {file.filename}")

                if not results:
                    error = "No valid image files were found in the folder."
                    logger.warning(error)
            except Exception as e:
                error = f"Error processing images: {str(e)}"
                logger.error(error)
    return render_template('index1.html', error=error, results=results)

@app.route('/stroke_info')
@login_required
def stroke_info():
    return render_template('stroke_info.html')

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)