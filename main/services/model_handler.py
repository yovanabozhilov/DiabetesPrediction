import pickle
import pandas as pd

MODEL_PATH = r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl'

def load_model():
    """Load the trained pipeline and evaluation metrics."""
    with open(MODEL_PATH, 'rb') as file:
        data = pickle.load(file)
    return data["model"], data["accuracy"]

def get_prediction(form_data):
    """Predict diabetes risk based on user input."""
    model, accuracy = load_model()

    # Define expected column order (same as in training data)
    columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
               "BMI", "DiabetesPedigreeFunction", "Age"]

    # Convert form data to list of floats (handle missing or invalid values)
    values = []
    for key in columns:
        raw_value = form_data.get(key, "")
        try:
            numeric_value = float(raw_value.strip()) if raw_value.strip() else 0
        except ValueError:
            print(f"Invalid input for {key}: {raw_value}. Using 0.")
            numeric_value = 0
        values.append(numeric_value)

    # Convert to DataFrame
    input_df = pd.DataFrame([values], columns=columns)

    # Debug logs
    print("Raw input values:", values)
    print("Input DataFrame:\n", input_df)

    # Predict using full pipeline (preprocessing + model)
    prediction_numeric = model.predict(input_df)[0]

    # Human-readable output
    prediction = (
        "You are at a higher risk of developing diabetes."
        if prediction_numeric == 1
        else "You are at a lower risk of developing diabetes."
    )

    return prediction, accuracy