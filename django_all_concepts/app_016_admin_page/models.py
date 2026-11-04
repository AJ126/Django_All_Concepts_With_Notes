from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="0000000000")

    def __str__(self):
        return self.name

class AdminPageModel(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ManyToManyField('user', related_name='users')  # Many-to-Many relationship with the 'user' model
    email = models.EmailField()
    message = models.TextField()
    info = models.CharField(max_length=100, blank=True)  # Optional field, can be left blank
    phone = models.CharField(max_length=15, default="0000000000")
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default=True)

    def __str__(self):
        return self.name