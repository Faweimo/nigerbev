from django import forms
from .models import Client, User
from django.contrib.auth.forms import AuthenticationForm

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = 'full_name',
        

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type',)

    def save(self,commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user     

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email 


class LoginForm(forms.Form):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'type':'email','class':'form-control','placeholder':'email'}))        
    password = forms.CharField(widget=forms.TextInput(attrs={'type':'password','class':'form-control','placeholder':'Password'}))
