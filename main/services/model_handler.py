import pickle
import pandas as pd

MODEL_PATH = r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl'

def load_model():
    """Load the trained model, preprocessor, and accuracy."""
    with open(MODEL_PATH, 'rb') as file:
        data = pickle.load(file)
    return data["model"], data["preprocessor"], data["accuracy"]


def get_prediction(form_data):
    """Predict diabetes risk based on user input."""
    model, preprocessor, accuracy = load_model()

    # Convert form data into a DataFrame
    columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
               "BMI", "DiabetesPedigreeFunction", "Age"]

    # Ensure all form values are converted to float
    values = []
    for key in form_data:
        value = form_data[key]
        try:
            # Convert to float, replace empty or invalid values with 0
            numeric_value = float(value.strip()) if value.strip() else 0
            values.append(numeric_value)
        except ValueError:
            # Handle invalid input by appending 0 (or use a different default if needed)
            print(f"Invalid input for {key}: {value}. Using 0 instead.")
            values.append(0)

    input_df = pd.DataFrame([values], columns=columns)

    # Print for debugging
    print("Form Data Converted to Numeric Values:", values)

    # Apply preprocessing to the input data
    input_df = preprocessor.transform(input_df)

    # Print for debugging
    print("Preprocessed Data:", input_df)

    # Make prediction
    pred = model.predict(input_df)
    prediction = "You are at a higher risk of developing diabetes." if pred == [1] else "You are at a lower risk of developing diabetes."

    return prediction, accuracy  # Returning model prediction and accuracy

