from django.db import models
from django.contrib.auth.models import User

class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree = models.FloatField()
    age = models.IntegerField()  
    prediction = models.CharField(max_length=50)
    accuracy = models.FloatField()  
    result_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction} ({self.result_date.date()})"
