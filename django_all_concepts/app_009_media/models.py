from django.db import models

# Create your models here.
class media(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField()