from tabnanny import verbose
from django.db import models

from accounts.models import User

class Approve(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    approved_by = models.IntegerField(default=0)

    def __str__(self) :
        return str(self.user.email)

    class Meta:        
        verbose_name = 'Approve'
        verbose_name_plural = 'Approves'    
