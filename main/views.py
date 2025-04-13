from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
import pickle
import logging
from .services.pdf_export import generate_pdf  
from .services.health_advice import get_health_advice
from .services.graphs import generate_insulin_graph, generate_bp_graph, generate_bmi_graph  
from .models import UserResult
from .forms import UserRegistrationForm, UserLoginForm, PredictionForm

logger = logging.getLogger(__name__)

def load_model():
    """Load the trained model and preprocessor."""
    with open(r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data['model'], data['preprocessor'], data['accuracy']

@login_required
def export_pdf(request):
    return generate_pdf(request.user)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Log successful registration with the user's username and IP
            logger.info(f"User registered successfully: {user.username} from IP: {get_client_ip(request)}")
            return redirect('profile')
        else:
            # Log invalid form submission with the IP address
            logger.warning(f"Registration failed: Invalid form submission from IP: {get_client_ip(request)} — errors: {form.errors}")
            messages.error(request, "Registration failed. Please check your input and try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"Login successful for user: {username} from IP: {get_client_ip(request)}")
                messages.success(request, "Login successful.")
                return redirect('predict')
            else:
                logger.warning(f"Login failed for username: {username} from IP: {get_client_ip(request)}")
                messages.error(request, "Invalid username or password.")
        else:
            logger.warning(f"Login form invalid from IP: {get_client_ip(request)} — errors: {form.errors}")
            messages.error(request, "Please check your username and password.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)

        if form.is_valid():
            return redirect('result')
        else:
            return render(request, 'predict.html', {'form': form})  
    else:
        form = PredictionForm()  
        return render(request, 'predict.html', {'form': form})


@login_required
def result(request):
    try:
        # Load the trained model and accuracy
        with open(r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl', 'rb') as file:
            data = pickle.load(file)
        model = data['model']
        accuracy = data['accuracy']

        # Extract form data (assumes query params: n1=..., n2=...)
        form_data = {
            'Pregnancies': request.GET.get('n1', ''),
            'Glucose': request.GET.get('n2', ''),
            'BloodPressure': request.GET.get('n3', ''),
            'SkinThickness': request.GET.get('n4', ''),
            'Insulin': request.GET.get('n5', ''),
            'BMI': request.GET.get('n6', ''),
            'DiabetesPedigreeFunction': request.GET.get('n7', ''),
            'Age': request.GET.get('n8', '')
        }

        # Prepare the values list and log the inputs
        values = []
        for key in form_data:
            raw_val = form_data[key]
            try:
                val = float(raw_val.strip()) if raw_val.strip() else 0
            except ValueError:
                logger.warning(f"Invalid input for {key}: '{raw_val}'. Defaulting to 0.")
                val = 0
            values.append(val)

        # Log the input data for prediction
        input_df = pd.DataFrame([values], columns=form_data.keys())
        logger.info(f"Prediction input for {request.user.username} from IP: {get_client_ip(request)}: {input_df.to_dict(orient='records')}")

        # Make the prediction
        pred = model.predict(input_df)[0]
        result1 = "You are at a higher risk of developing diabetes." if pred == 1 else "You are at a lower risk of developing diabetes."

        # Save the result in the database
        UserResult.objects.create(
            user=request.user,
            pregnancies=input_df.at[0, 'Pregnancies'],
            glucose=input_df.at[0, 'Glucose'],
            blood_pressure=input_df.at[0, 'BloodPressure'],
            skin_thickness=input_df.at[0, 'SkinThickness'],
            insulin=input_df.at[0, 'Insulin'],
            bmi=input_df.at[0, 'BMI'],
            diabetes_pedigree=input_df.at[0, 'DiabetesPedigreeFunction'],
            age=input_df.at[0, 'Age'],
            prediction=result1,
            accuracy=round(accuracy * 100, 2)
        )

        # Log the result saving
        logger.info(f"Prediction saved for {request.user.username} from IP: {get_client_ip(request)}: {result1} (Accuracy: {round(accuracy * 100, 2)}%)")

        # Generate health advice and graphs
        advice = get_health_advice(values)
        insulin_graph_html = generate_insulin_graph(values)
        bp_graph_html = generate_bp_graph(values)
        bmi_graph_html = generate_bmi_graph(values)

        # Return the result view with the context
        return render(request, 'result.html', {
            "result2": result1,
            "accuracy": round(accuracy * 100, 2),
            "form_data": form_data,
            "insulin_graph_html": insulin_graph_html,
            "bp_graph_html": bp_graph_html,
            "bmi_graph_html": bmi_graph_html,
            "advice": advice
        })

    except Exception as e:
        # Log the error
        logger.error(f"Error during prediction processing for {request.user.username} from IP: {get_client_ip(request)}: {str(e)}", exc_info=True)

        # Show error message to the user
        messages.error(request, "An unexpected error occurred while processing your prediction. Please try again later.")
        
        # Redirect the user back to the prediction page
        return redirect('predict')


@login_required
def profile(request):
    user_results = UserResult.objects.filter(user=request.user)

    # Generate health advice for each result
    results_with_advice = []
    for result in user_results:
        # Gather the values from the result
        values = [
            result.pregnancies,
            result.glucose,
            result.blood_pressure,
            result.skin_thickness,
            result.insulin,
            result.bmi,
            result.diabetes_pedigree,
            result.age
        ]
        
        # Get the health advice for the prediction result
        advice = get_health_advice(values)

        # Attach the health advice to the result
        results_with_advice.append({
            'result': result,
            'advice': advice
        })

    return render(request, 'profile.html', {'results_with_advice': results_with_advice})


@login_required
def delete_prediction(request, result_id):
    try:
        result = get_object_or_404(UserResult, id=result_id, user=request.user)
        result.delete()
        logger.info(f"Prediction with ID {result_id} deleted by user {request.user.username} from IP: {get_client_ip(request)}")
        messages.success(request, "Your prediction has been deleted successfully.")
        return redirect('profile')
    except Exception as e:
        logger.error(f"Error deleting prediction with ID {result_id} for user {request.user.username} from IP: {get_client_ip(request)}: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while trying to delete the prediction.")
        return redirect('profile')

def logout_view(request):
    logger.info(f"User logged out: {request.user.username} from IP: {get_client_ip(request)}")
    logout(request)
    return redirect('home')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]  # First IP in the list
    return request.META.get('REMOTE_ADDR')