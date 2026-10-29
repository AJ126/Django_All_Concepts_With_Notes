from django.db import models
import datetime

# Create your models here.
class ormInfo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    date = models.DateField(default=datetime.datetime.now)
    active = models.BooleanField()
    duration = models.DurationField()
    url = models.URLField()