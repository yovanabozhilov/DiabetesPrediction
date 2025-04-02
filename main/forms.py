from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PredictionForm(forms.Form):
    pregnancies = forms.IntegerField(min_value=0, max_value=17, error_messages={
        'min_value': 'Pregnancies cannot be negative.',
        'max_value': 'Pregnancies cannot exceed 17.'
    })
    glucose = forms.IntegerField(min_value=0, max_value=199, error_messages={
        'min_value': 'Glucose level cannot be less than 0.',
        'max_value': 'Glucose level cannot exceed 199.'
    })
    blood_pressure = forms.IntegerField(min_value=0, max_value=122, error_messages={
        'min_value': 'Blood pressure cannot be less than 0.',
        'max_value': 'Blood pressure cannot exceed 122.'
    })
    skin_thickness = forms.IntegerField(min_value=0, max_value=99, error_messages={
        'min_value': 'Skin thickness cannot be less than 0.',
        'max_value': 'Skin thickness cannot exceed 99.'
    })
    insulin = forms.IntegerField(min_value=0, max_value=846, error_messages={
        'min_value': 'Insulin cannot be less than 0.',
        'max_value': 'Insulin cannot exceed 846.'
    })
    bmi = forms.FloatField(min_value=0, max_value=67.1, error_messages={
        'min_value': 'BMI cannot be less than 0.',
        'max_value': 'BMI cannot exceed 67.1.'
    })
    diabetes_pedigree = forms.FloatField(min_value=0.078, max_value=2.42, error_messages={
        'min_value': 'Diabetes Pedigree cannot be less than 0.078.',
        'max_value': 'Diabetes Pedigree cannot exceed 2.42.'
    })
    age = forms.IntegerField(min_value=21, max_value=81, error_messages={
        'min_value': 'Age cannot be less than 21.',
        'max_value': 'Age cannot exceed 81.'
    })