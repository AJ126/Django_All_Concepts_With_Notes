from django.db import models

# Create your models here.
class demoData(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class dateModel(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
