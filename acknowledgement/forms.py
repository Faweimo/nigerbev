from django import forms 

from .models import Demo    

class DemoForm(forms.ModelForm):
    class Meta:
        model = Demo
        fields = '__all__'
        widgets = {
            'client':forms.TextInput(attrs={
                'type':'hidden',
            }),
            
        }  