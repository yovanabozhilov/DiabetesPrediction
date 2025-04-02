# Diabetes Prediction Project

## Overview
This project is a machine learning-based web application for predicting diabetes using patient health data. The model is trained on a dataset containing various health parameters and predicts whether an individual has diabetes.

## Features
- User Authentication: Register and log in securely.
- Diabetes Prediction: Input health metrics to get predictions.
- Prediction History: View all previous predictions with date and time.
- Delete Predictions: Remove unwanted predictions from the profile.
- Data Visualization: Graphs and insights using Plotly.
- Download Reports: Save predictions as PDFs.
- Responsive UI: Django-based, user-friendly interface.

## Technologies Used
- **Backend**: Django, Python
- **Machine Learning**: Scikit-learn, Pandas, NumPy, Custom Random Forest Implementation
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Django 5.1+
- Virtualenv (optional but recommended)
- Git

### Setup Steps
1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   cd DiabetesPrediction
   ```
2. **Create and Activate Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run Migrations**:
   ```sh
   python manage.py migrate
   ```
5. **Train the Model**:
   ```sh
   python predictor/train_model.py
   ```
6. **Run the Server**:
   ```sh
   python manage.py runserver
   ```
7. **Access the Application**:
   Open `http://127.0.0.1:8000/` in your browser.

### Usage
- Register/Login to access prediction features.
- Navigate to the prediction page, input your health data, and get results.
- View past predictions on your profile page.
- Download or delete predictions as needed.

## Model Training
The model is trained using the `train_model.py` script, which:
- Reads and preprocesses the diabetes dataset
- Handles missing values using median imputation
- Splits data into training and test sets
- Trains a custom RandomForest model
- Saves the trained model for predictions

If you need to retrain the model:
1. Ensure you have the dataset diabetes.csv in the `predictor/` folder.
2. Run the training script:
```sh
python predictor/train_model.py
```
3. The trained model (`diabetes_model.pkl`) will be saved in `predictor/`.

