from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
import logging
from .services.pdf_export import generate_pdf  
from .services.health_advice import get_health_advice
from .services.graphs import generate_insulin_graph, generate_bp_graph, generate_bmi_graph  
from .models import UserResult
from .forms import UserRegistrationForm, UserLoginForm, PredictionForm
from .services.model_handler import get_prediction

logger = logging.getLogger(__name__)

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
            logger.info(f"User registered successfully: {user.username} from IP: {get_client_ip(request)}")
            return redirect('profile')
        else:
            logger.warning(f"Registration failed: Invalid form submission from IP: {get_client_ip(request)} — errors: {form.errors}")
            messages.error(request, "Registration failed. Please check your input and try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    list(get_messages(request)) 
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

        prediction, values, accuracy = get_prediction(form_data)

        UserResult.objects.create(
            user=request.user,
            pregnancies=values[0],
            glucose=values[1],
            blood_pressure=values[2],
            skin_thickness=values[3],
            insulin=values[4],
            bmi=values[5],
            diabetes_pedigree=values[6],
            age=values[7],
            prediction=prediction,
            accuracy=round(accuracy * 100, 2)
        )

        logger.info(f"Prediction saved for {request.user.username} from IP: {get_client_ip(request)}: {prediction} (Accuracy: {round(accuracy * 100, 2)}%)")

        advice = get_health_advice(values)
        insulin_graph_html = generate_insulin_graph(values)
        bp_graph_html = generate_bp_graph(values)
        bmi_graph_html = generate_bmi_graph(values)

        return render(request, 'result.html', {
            "result2": prediction,
            "accuracy": round(accuracy * 100, 2),
            "form_data": form_data,
            "insulin_graph_html": insulin_graph_html,
            "bp_graph_html": bp_graph_html,
            "bmi_graph_html": bmi_graph_html,
            "advice": advice
        })

    except Exception as e:
        logger.error(f"Error during prediction for {request.user.username} from IP: {get_client_ip(request)}: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred while processing your prediction. Please try again later.")
        return redirect('predict')

@login_required
def profile(request):
    user_results = UserResult.objects.filter(user=request.user)

    results_with_advice = []
    for result in user_results:
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
        
        advice = get_health_advice(values)

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

    list(get_messages(request))

    return redirect('home')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0] 
    return request.META.get('REMOTE_ADDR')
