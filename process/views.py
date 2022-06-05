import email
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import User
from django.contrib.auth.decorators import login_required
from process.models import LeaveRequest
from .forms import LeaveRequestForm


import os
from re import template
from urllib import response
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from accounts.models import User

from process.models import LeaveRequest
  

""" PDF  """

def staff_request_pdf(request,leave_id):
    # user = User.objects.get(id=request.user.id)
    leave = LeaveRequest.objects.get(id=leave_id)
    template_path='process/staff_request_slip.html'
    context = {
        'leave':leave,
        # 'user':user
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename = "staff_request_slip.pdf"'

    # template and render it 
    template = get_template(template_path)
    html = template.render(context)

    pisa_create = pisa.CreatePDF(
        html,
        dest=response
    )
    if pisa_create.err:
        return HttpResponse('Error in displaying')
    return response  



""" 
HOME PAGE """

def home(request):
    return render(request,'process/home.html')




def index(request):
        
    if request.method == 'POST':
        leave_start = request.POST['leave_start']
        leave_end = request.POST['leave_end']      
        
        user = User.objects.get(id=request.user.id)
        
        leave = LeaveRequest(user=user,leave_start=leave_start,leave_end=leave_end)        
        leave.save()
        print('success')       
        return redirect('table_leave')
   
    return render (request,'process/index.html')

""" MANAGE TABLE """
def table_leave(request):
    leave = LeaveRequest.objects.get(user=request.user)
    context = {
        'leave':leave
    }
    return render(request,'process/table.html',context)


""" 
TEAM LEADER ADMIN PAGE  """
def team_leader_page(request):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        user = User.objects.filter(user_type=4).get(user_type=4)        
        leave = LeaveRequest.objects.filter(user=user)
        context = {
            'leaves':leave
        }    
    return render(request,'process/team.html',context)


""" SUPERVISOR ADMIN PAGE """     
def supevisor_leader_page(request):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
        user = User.objects.filter(user_type=4).get(user_type=4)        
        leave = LeaveRequest.objects.filter(user=user)
        context = {
            'leaves':leave
        }    
    return render(request,'process/supervisor.html',context)


""" MANAGER ADMIN PAGE """     
def manager_leader_page(request):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:
        user = User.objects.filter(user_type=4).get(user_type=4)        
        leave = LeaveRequest.objects.filter(user=user)
        
        context = {
            'leaves':leave
        }    
    return render(request,'process/manager.html',context)


""" APPROVE LEAVE BY TEAM LEADER  """
def approve_team_leader(request, team_id):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=team_id)    
        leave.leave_status_isteamleader = 1
        leave.save()
        print('leave approved')
        return redirect('table_leave')


""" DISAPPROVE LEAVE BY TEAM LEADER  """
def disapprove_team_leader(request, team_id):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=team_id)    
        leave.leave_status_isteamleader = 2
        leave.save()
        print('leave approved')
        return redirect('table_leave')



""" APPROVE LEAVE BY SUPERVISOR  """
def approve_supose(request, supose_id):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=supose_id)    
        leave.leave_status_issupervisor = 1
        leave.save()
        print('leave disapproved')
        return redirect('table_leave')


""" DISAPPROVE LEAVE BY SUPERVISOR  """
def disapprove_supose(request, supose_id):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=supose_id)    
        leave.leave_status_issupervisor = 2
        leave.save()
        print('leave disapproved')
        return redirect('table_leave')


""" APPROVE LEAVE BY MANAGER  """
def approve_manager(request, manager_id):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=manager_id)    
        leave.leave_status_ismanager = 1
        leave.save()
        print('leave approved')
        return redirect('table_leave')
               

""" DISAPPROVE LEAVE BY MANAGER  """
def disapprove_manager(request, manager_id):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:
        leave = LeaveRequest.objects.get(id=manager_id)    
        leave.leave_status_ismanager = 2
        leave.save()
        print('leave disapproved')
        return redirect('table_leave')
                              