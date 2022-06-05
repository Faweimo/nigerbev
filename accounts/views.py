from curses.ascii import US
import email
from http import client
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from accounts.forms import RegisterForm, LoginForm, ClientForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from accounts.models import Client, User
from voucher.models import PaymentRequisitionVoucher
import requests

""" ACCOUNT REGISTRATION """
def register(request):
    if not request.user.is_authenticated:
        return HttpResponse('Oops Seems what you are looking for is not here')
    elif not request.user.user_type == 1:    
        return HttpResponse('Central Admin can register')
    else:    
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            
            if form.is_valid():
                user = form.save(commit=False)
                
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                password2 = form.cleaned_data.get('password2')
                user.set_password(form.cleaned_data['password'])
                user.is_active = True
                user.is_staff = True
                # user.user_type =4
                if User.objects.filter(email = user.email).exists():
                    messages.warning(request, 'Email Already exists, Please use a different email')
                    return redirect('register')
                if password != password2:
                    messages.error(request, 'Password do not match, Please make sure it matches')    
                    return redirect('register')
                user.save()
                        
                print('success')
                messages.success(request, 'Account created successfully')
                return redirect('central_page')

            else:
                print('failed') 
                messages.error(request, 'Failed to register')
                return redirect('register')   
        else:
            form = RegisterForm()
            
        context = {
            'form':form,       
        }  

    return render(request,'accounts/register.html',context)


""" LOGIN VIEW """
def login(request):    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)    
        
        if form.is_valid():
            user = form
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(form=form,email=email, password=password)                                  
            
        if user is not None:            
            auth.login(request,user)
            if request.user.user_type == 1:
                messages.success(request, 'You are now logged in')
                return redirect('central_page')
            elif request.user.user_type == 2:
                messages.success(request, 'You are now logged in')
                return redirect('acknowlege')   
            elif request.user.user_type == 3:
                messages.success(request, 'You are now logged in')
                return redirect('manager_page')
            elif request.user.user_type == 4:
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')      
              
            
            messages.success(request, 'You are logged in')
            return redirect('dashboard')
        else:
            form = LoginForm()
            
            messages.error(request, 'Unable to login, Check your email and password')
            return redirect('login')        
    else:
        form = LoginForm()
    context = {
        'form':form
    }    
    return render(request, 'accounts/login.html',context)    


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')


""" CLIENTS DASHBOARD """   
@login_required 
def dashboard(request): 
    if request.user.user_type !=4:   
        return HttpResponse('You are not allow to view this page')
    user = User.objects.get(id=request.user.id)
    vouchers = PaymentRequisitionVoucher.objects.filter(client__user= user, is_deleted=False).order_by('-voucher_updated_at').order_by('-voucher_created_at')
    
    context = {        
        'vouchers':vouchers
    }
    return render(request, 'accounts/dashboard.html',context)