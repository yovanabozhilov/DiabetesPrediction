def get_health_advice(values):
    """Provide personalized health advice based on user input values."""
    advice = []

    bmi = values[5]
    if bmi >= 30:
        advice.append("Your BMI is high. Consider following a balanced diet and exercise regularly.")
    elif bmi >= 25:
        advice.append("You have an elevated BMI. Try to manage your weight through a healthy lifestyle.")

    insulin = values[4]
    if insulin >= 26:
        advice.append("Your insulin level is high. Try reducing stress, sugar intake and improve your exercise routine.")

    age = values[7]
    if age > 45:
        advice.append("You are over 45 years old, and it's essential to monitor your health regularly.")

    # If there is no advice, provide a positive default message
    if not advice:
        advice.append("Your health seems great! Keep up the good work.")

    return advice
