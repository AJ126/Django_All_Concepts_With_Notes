from django.db import models
from django.urls import reverse

# Create your models here.
class testInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def get_absolute_url(self):
            return reverse("listview")
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    