from django.db import models
import datetime

# Create your models here.
class media(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField()

class images(models.Model):
    image = models.ImageField(upload_to='images')
    date = models.DateTimeField(default=datetime.datetime.now())