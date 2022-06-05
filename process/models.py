from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
import datetime
import pandas as pd
import numpy as np

class LeaveRequest(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    leave_start = models.DateField(blank=True,null=True)
    leave_end = models.DateField(blank=True,null=True)
    total_days = models.CharField(blank=True,null=True,max_length=100)
    leave_status_isteamleader = models.IntegerField(default=0)
    leave_status_issupervisor = models.IntegerField(default=0)
    leave_status_ismanager = models.IntegerField(default=0)

    def __str__(self):
        return str(f'{self.user.email }')

    def save(self,*args,**kwargs):
        self.total_days = 0
        leave_end = pd.to_datetime(self.leave_end).date()
        leave_start = pd.to_datetime(self.leave_start).date()
        self.total_days = np.busday_count(leave_start,leave_end,holidays=[leave_start,leave_end] )      

        super(LeaveRequest,self).save(*args,**kwargs)

    class Meta:        
        verbose_name = _('Leave Request')
        verbose_name_plural = _('Leave Requests')
