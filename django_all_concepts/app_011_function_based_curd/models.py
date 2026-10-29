from django.db import models

# Create your models here.
class customer(models.Model):
    profilepic = models.ImageField(upload_to='customerPics',  blank=True, null = True)
    name = models.CharField(max_length=100)
    customerId = models.IntegerField()
    details = models.CharField(max_length=100)
    status = models.BooleanField(default=False)