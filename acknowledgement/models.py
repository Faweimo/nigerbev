from ast import Return
from re import A
from django.db import models

from accounts.models import Client, User
from approval.models import Approve


class Acknlowledge(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    acknlowledged_by = models.IntegerField(default=0)

    def __str__(self) :
        return str(self.user.email)

    class Meta:        
        verbose_name = 'Acknlowledge'
        verbose_name_plural = 'Acknlowledges'   

class Demo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    description = models.TextField()
    acknowlege_by = models.ForeignKey(Acknlowledge,on_delete=models.DO_NOTHING)
    approved_by = models.ForeignKey(Approve,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.id

    class Meta:
    
       
        verbose_name = 'Demo'
        verbose_name_plural = 'Demos'        