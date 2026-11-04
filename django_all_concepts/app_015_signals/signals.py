from django.db.models.signals import post_save
from django.dispatch import receiver
from app_015_signals.models import *

@receiver(post_save, sender=customer)
def create_customer_profile(sender, instance, created, **kwargs):
    print('sender.........',sender )
    print('instance.........', instance)
    print('created.........', created)
    if created:
        customerInfo.objects.create(customer_name = instance.name)
        print("Customer info created successfully!")