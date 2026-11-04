from django.db import models

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=100)
    customer_id = models.IntegerField()

class customerInfo(models.Model):
    customer_name = models.CharField(max_length=100)
    detail = models.TextField()