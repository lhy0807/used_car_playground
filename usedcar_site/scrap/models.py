from django.db import models

# Create your models here.
class ModelCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    year = models.IntegerField()
    make = models.CharField(max_length=10)
    model = models.CharField(max_length=50)