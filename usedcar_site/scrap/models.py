from django.db import models

# Create your models here.
class ModelCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    year = models.IntegerField()
    make = models.CharField(max_length=10)
    model = models.CharField(max_length=50)

class Record(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=1024)
    model = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    mileage = models.CharField(max_length=10)