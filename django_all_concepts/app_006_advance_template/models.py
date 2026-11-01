from django.db import models

# Create your models here.
class userInfo(models.Model):
    name = models.CharField(max_length=100)
    data = models.CharField(max_length=200)
    details = models.TextField()
    date = models.DateField()