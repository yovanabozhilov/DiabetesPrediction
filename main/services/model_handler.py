import pickle
import pandas as pd

MODEL_PATH = r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl'

def load_model():
    with open(MODEL_PATH, 'rb') as file:
        data = pickle.load(file)
    return data["model"], data["imputer"], data["scaler"], data.get("accuracy", 0)

def get_prediction(form_data):
    model, imputer, scaler, accuracy = load_model()

    columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
               "BMI", "DiabetesPedigreeFunction", "Age"]

    values = []
    for key in columns:
        raw_value = form_data.get(key, "")
        try:
            numeric_value = float(raw_value.strip()) if raw_value.strip() else 0
        except ValueError:
            print(f"Invalid input for {key}: {raw_value}. Using 0.")
            numeric_value = 0
        values.append(numeric_value)

    input_df = pd.DataFrame([values], columns=columns)

    input_processed = scaler.transform(imputer.transform(input_df))

    prediction_numeric = model.predict(input_processed)[0]

    prediction = (
        "You are at a higher risk of developing diabetes."
        if prediction_numeric == 1
        else "You are at a lower risk of developing diabetes."
    )

    return prediction, values, accuracy
