from multiprocessing.reduction import register
from django.contrib import admin
from .models import LeaveRequest

admin.site.register(LeaveRequest)