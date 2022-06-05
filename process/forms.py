import imp
from pyexpat import model
from django import forms
from .models import LeaveRequest
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ('user','leave_start', 'leave_end')
