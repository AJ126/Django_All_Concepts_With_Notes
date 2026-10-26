from django.db import models

# Create your models here.
class testData(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()