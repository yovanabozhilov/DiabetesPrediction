from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
import numpy as np
import pickle
from .services.pdf_export import generate_pdf  
from .services.health_advice import get_health_advice
from .services.graphs import generate_insulin_graph, generate_bp_graph, generate_bmi_graph  
from .models import UserResult
from .forms import UserRegistrationForm, UserLoginForm, PredictionForm
from django.http import HttpResponse

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
            return redirect('profile')
        else:
            messages.error(request, "Registration failed.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('predict')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            return redirect('result')
        else:
            return render(request, 'predict.html', {'form': form})  
    else:
        form = PredictionForm()  
        return render(request, 'predict.html', {'form': form})


@login_required
def result(request):
    # Load the model, preprocessor, and accuracy
    model, preprocessor, accuracy = load_model()

    # Form data from the user input (assume it comes from GET or POST)
    form_data = {
        'n1': request.GET.get('n1', ''),  # Pregnancies
        'n2': request.GET.get('n2', ''),  # Glucose
        'n3': request.GET.get('n3', ''),  # BloodPressure
        'n4': request.GET.get('n4', ''),  # SkinThickness
        'n5': request.GET.get('n5', ''),  # Insulin
        'n6': request.GET.get('n6', ''),  # BMI
        'n7': request.GET.get('n7', ''),  # DiabetesPedigreeFunction
        'n8': request.GET.get('n8', '')   # Age
    }

    # Convert the form values to numeric, and fill empty fields with zero
    values = [float(form_data[key]) if form_data[key] else 0 for key in form_data]

    # Ensure the correct order of features: Only the relevant columns for prediction
    # Create the array in the order the model expects (the same as used for training)
    input_features = np.array(values).reshape(1, -1)  # Make sure it's a 2D array for prediction

    # Apply preprocessing to the relevant columns (imputation)
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    input_features[:, [1, 2, 3, 4, 5]] = preprocessor.transform(input_features[:, [1, 2, 3, 4, 5]])

    # Make a prediction
    pred = model.predict(input_features)

    # Generate the prediction result
    result1 = "You are at a higher risk of developing diabetes." if pred == [1] else "You are at a lower risk of developing diabetes."

    # Save the result to the database
    UserResult.objects.create(
        user=request.user,
        pregnancies=input_features[0][0],
        glucose=input_features[0][1],
        blood_pressure=input_features[0][2],
        skin_thickness=input_features[0][3],
        insulin=input_features[0][4],
        bmi=input_features[0][5],
        diabetes_pedigree=input_features[0][6],
        age=input_features[0][7],
        prediction=result1,
        accuracy=round(accuracy * 100, 2)
    )

    # Generate advice
    advice = get_health_advice(input_features[0])


    # Convert figures to HTML
    insulin_graph_html = generate_insulin_graph(values)  # Pass values to the graph function
    bp_graph_html = generate_bp_graph(values)  # Pass values to the graph function
    bmi_graph_html = generate_bmi_graph(values)  # Pass values to the graph function

    return render(request, 'result.html', {
        "result2": result1,
        "accuracy": round(accuracy * 100, 2),
        "form_data": form_data,
        "insulin_graph_html": insulin_graph_html,
        "bp_graph_html": bp_graph_html,
        "bmi_graph_html": bmi_graph_html,
        "advice": advice
    })

@login_required
def profile(request):
    user_results = UserResult.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_results': user_results})

@login_required
def delete_prediction(request, result_id):
    result = get_object_or_404(UserResult, id=result_id, user=request.user)
    result.delete()
    messages.success(request, "Your prediction has been deleted successfully.")
    return redirect('profile')

def logout_view(request):
    logout(request)  
    return redirect('home')
