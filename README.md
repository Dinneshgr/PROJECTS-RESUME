Data Science Portfolio
Welcome to my Data Science Portfolio! This repository showcases three projects highlighting my skills in machine learning, deep learning, and data visualization using Python and Power BI. As a Data Science Intern, I’ve focused on building end-to-end solutions that combine predictive modeling, data analysis, and user-friendly interfaces. These projects demonstrate my ability to tackle real-world problems across domains like sports analytics, deep learning applications, and financial insights—skills relevant to roles like Data Scientist or Business Analyst.

Projects
1. Formula 1 Race Winner Prediction Model

Description: A machine learning project to predict the likelihood of a Formula 1 driver winning a race using historical data (e.g., race results, driver standings, qualifying times). The model, a tuned Random Forest classifier with SMOTE for imbalanced data, achieved an AUC score of ~0.85. It includes a Flask web application with a Tailwind CSS front-end for real-time predictions.
Purpose: To provide a predictive tool for F1 fans, analysts, or teams to assess race outcomes based on features like grid position and driver performance.
Technologies: Python, Pandas, Scikit-learn, Flask, Tailwind CSS, Joblib.
How to Run:
Clone the repository: git clone <repository-url>.
Navigate to the f1_prediction_app directory.
Install dependencies: pip install -r requirements.txt.
Ensure the f1_rf_model.pkl file is in the directory (generated from the Jupyter Notebook).
Run the app: python app.py.
Access the web app at http://127.0.0.1:5000/.


Files: app.py, templates/index.html, requirements.txt, f1_rf_model.pkl.
Relevance: Demonstrates end-to-end machine learning, web development, and translating insights into user-friendly tools.

2. Deep Learning Image Classification Project

Description: A deep learning project to classify images (e.g., identifying car types or F1 team logos) using a Convolutional Neural Network (CNN). The model was trained on a custom dataset, achieving ~90% accuracy on the test set, and includes data augmentation for robustness.
Purpose: To explore deep learning techniques for computer vision tasks, with potential applications in autonomous driving or sports branding analysis.
Technologies: Python, TensorFlow/Keras, OpenCV, Matplotlib.
How to Run:
Clone the repository: git clone <repository-url>.
Navigate to the project directory.
Install dependencies: pip install tensorflow opencv-python matplotlib numpy.
Ensure the dataset is in the data folder.
Run the script: python train_model.py.


Files: train_model.py, data/ (dataset), model.h5 (trained model).
Relevance: Showcases deep learning expertise, data preprocessing, and model evaluation for advanced analytics.

3. GPU Market Stock Analysis Dashboard

Description: A Power BI dashboard analyzing GPU market trends and stock performance using sales data, stock prices, and market reports. It includes interactive visuals like line charts for price trends and slicers for filtering by brand or time period.
Purpose: To provide actionable insights for investors or tech companies on GPU market dynamics and stock movements.
Technologies: Power BI, Excel, DAX.
How to Run:
Download the .pbix file from the repository.
Open with Power BI Desktop.
Load the included dataset (gpu_data.csv) or connect to your data source.
Explore the dashboard interactively.


Files: gpu_dashboard.pbix, gpu_data.csv.
Relevance: Highlights data visualization, business intelligence, and stakeholder reporting skills.

Setup Instructions

Prerequisites:

Python 3.7+ for Python projects.
Power BI Desktop for the dashboard.
Git for cloning the repository.


Installation:

Install Python dependencies using pip install -r requirements.txt for Python projects.
Ensure datasets and model files are placed in the correct directories as specified.


Running Projects:

Follow the "How to Run" steps for each project.
For deployment (optional), use platforms like Heroku for the Flask app or Power BI Service for the dashboard.



Skills Demonstrated

Machine Learning: Feature engineering, model tuning, handling imbalanced data.
Deep Learning: CNNs, data augmentation, model training.
Data Visualization: Interactive dashboards, statistical plots.
Web Development: Flask, HTML, Tailwind CSS.
Tools: Python (Pandas, Scikit-learn, TensorFlow), Power BI, Git.

Future Improvements

F1 Prediction Model: Add track-specific features (e.g., weather, circuit length) or deploy online.
Deep Learning Project: Expand the dataset or implement transfer learning.
Power BI Dashboard: Integrate real-time stock data via APIs.

