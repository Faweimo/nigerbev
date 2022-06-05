from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client, User


@receiver(post_save, sender=User)        
def create_user_profile(sender,instance,created,**kwargs):
  
    if created:
        if instance.user_type==4:
            Client.objects.create(user=instance)
            instance.save()
