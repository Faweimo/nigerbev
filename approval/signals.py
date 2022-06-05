from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from approval.models import Approve



@receiver(post_save, sender=User)        
def create_user_profile(sender,instance,created,**kwargs):
  
    if created:
        if instance.user_type==3:
            Approve.objects.create(user=instance)
            instance.save()            