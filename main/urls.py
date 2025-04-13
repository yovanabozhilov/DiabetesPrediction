from django.views.generic import RedirectView
from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),  
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('predict/', views.predict, name='predict'),  
    path('result/', views.result, name='result'), 
    path('profile/', views.profile, name='profile'), 
    path('delete_prediction/<int:result_id>/', views.delete_prediction, name='delete_prediction'), 
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]
