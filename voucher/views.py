import csv
from curses.ascii import HT
import email
from http import client
from pydoc import cli
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from requests import request
from accounts.models import User , Client
from approval.models import Approve
import voucher
from voucher.models import PaymentRequisitionVoucher, PaymentVerification, Tested, UploadMember
from .forms import PaymentRequisitionForm, UpdatePaymentRequisitionForm, UploadMemberForm,TestingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# PDF 
from django.template.loader import get_template
from xhtml2pdf import pisa

# Email configurations
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def testing_page(request):
    users = User.objects.all()
    form = TestingForm()
    context = {
        'users':users,
        'form':form
    }
    return render(request, 'voucher/test.html',context)

def testing_save(request):
    form = TestingForm()
    print('error2')
    if request.method == ' POST':
        # user = request.POST.get('user')
        # approved_by = request.POST['approved_by']
        # acknownlege_by = request.POST['acknownlege_by']
        # mtext = request.POST['mtext']

        # user_obj = User.objects.get(id = request.user.id)
        # approve_obj = Approve.objects.get(user = approved_by)
        # acknownlege_obj = User.objects.get(email = acknownlege_by)

        # print(user_obj)
        # print(approve_obj)
        # print(acknownlege_obj)

        # testing = Tested(user=user, approved_by=approve_obj,acknownlege_obj=acknownlege_by,mtext=mtext)

        # testing.save()
        # print('success')

        form = TestingForm(request.POST or  None)

        if form.is_valid():
            try:
                form.save()
                print('save')
            except:
                print('bad')    

        else:
            print('error')

    return render(request, 'voucher/test.html',{'form':form})
    

""" Client making a request """
@login_required
def requestclient(request):
    user = User.objects.get(id=request.user.id)
    user_obj = User.objects.all()
    client_obj = Client.objects.get(user=request.user.id)
    payment = PaymentRequisitionVoucher.objects.filter(client=client_obj).order_by('-voucher_updated_at')
    
    context = {
        'payment':payment,
        'client':client_obj,
        'user':user,
        'user_obj':user_obj,
        # 'approve':approve
    }
    return render(request,'voucher/requestvouccher.html',context) 


def requestclient_save(request):
  
    if request.method != 'POST':
        print('Method not allowed')
    else:
        
        payee = request.POST['payee']    
        account_number = request.POST['account_number']
        qty = request.POST['qty']
        rate = request.POST['rate']
        details = request.POST['details']
        amount = request.POST['amount']
        qty_2 = request.POST['qty_2']
        rate_2 = request.POST['rate_2']
        details_2 = request.POST['details_2']
        amount_2 = request.POST['amount_2']
        qty_3 = request.POST['qty_3']
        rate_3 = request.POST['rate_3']
        details_3 = request.POST['details_3']
        amount_3 = request.POST['amount_3']
        qty_4 = request.POST['qty_4']
        rate_4 = request.POST['rate_4']
        details_4 = request.POST['details_4']
        amount_4 = request.POST['amount_4']
        qty_5 = request.POST['qty_5']
        rate_5 = request.POST['rate_5']
        details_5 = request.POST['details_5']
        amount_5 = request.POST['amount_5']
        total = request.POST['total']
        amount_in_words = request.POST['amount_in_words']
        requested_by = request.POST['requested_by']
        acknowlege_email = request.POST['acknowlege_email']
        approve_email = request.POST['approve_email']
       
        
        client_obj = Client.objects.get(user = request.user.id)

        # saving to DB        
        payment = PaymentRequisitionVoucher.objects.create(client=client_obj,payee=payee,account_number=account_number,qty=qty,rate=rate,details=details,amount=amount,qty_2=qty_2,rate_2=rate_2,details_2=details_2,amount_2=amount_2,qty_3=qty_3,rate_3=rate_3,details_3=details_3,amount_3=amount_3,qty_4=qty_4,rate_4=rate_4,details_4=details_4,amount_4=amount_4,qty_5=qty_5,rate_5=rate_5,details_5=details_5,amount_5=amount_5,total=total,amount_in_words=amount_in_words,requested_by=requested_by,acknowledge_by=0,approved_by=0,approve_email=approve_email,acknowlege_email=acknowlege_email)       
        payment.save()        
        
        # SEND EMAIL FOR APPROVAL AND ACKNOWLEGE 
        
        acknowlege_email = request.POST.get('acknowlege_email')
        approve_email = request.POST.get('approve_email')       
        voucher = PaymentRequisitionVoucher.objects.get(id=payment.id)       
        
        current_site = get_current_site(request)
        mail_subject = 'Hi, you have what you want to acknowlege'
        
        html_message = render_to_string('voucher/email_text.html', {
            'acknowlege_email': acknowlege_email,
            'approve_email':approve_email,            
            'voucher':voucher,            
            'domain':current_site,
        })
        to = acknowlege_email
        send_email = EmailMessage(mail_subject, html_message, to=[to])
        send_email.content_subtype = "html"
        send_email.send()
        
        # APPROVAL EMAIL 
        current_site = get_current_site(request)
        mail_subject = 'Hi, you have what to approve'
        
        html_message = render_to_string('voucher/email_approve_text.html', {
            'acknowlege_email': acknowlege_email,
            'approve_email':approve_email,            
            'voucher':voucher,            
            'domain':current_site,
        })
        to = approve_email
        send_email = EmailMessage(mail_subject, html_message, to=[to])
        send_email.content_subtype = "html"
        send_email.send()
        messages.success(request,'Voucher Received Successfully, Awaiting Approval to print')
        return redirect('dashboard')
        
    return render(request,'voucher/requestvouccher.html')        


""" TOTAL APPROVED VOUCHER """
def total_approved(request):
    if not request.user.user_type == 4:
        return HttpResponse('You are not allowed to view this page')    
    else:    
        user = User.objects.get(id=request.user.id)
        voucher = PaymentRequisitionVoucher.objects.filter(approved_by=1, acknowledge_by=0).filter(client__user=user).order_by('-voucher_updated_at')       
        context = {
            'vouchers':voucher
        }
    return render(request,'voucher/total_approved.html',context)


""" TOTAL PENDING VOUCHER """
def pending_approved(request):    
    if not request.user.user_type == 4:
        return HttpResponse('You are not allowed to view this page')
    else:

        user = User.objects.get(id=request.user.id)
        voucher = PaymentRequisitionVoucher.objects.filter(approved_by=0, acknowledge_by=0).filter(client__user=user).order_by('-voucher_updated_at')
        context = {
            'vouchers':voucher
        }
    return render(request,'voucher/total_pending.html',context)


""" TOTAL DISAPROVED VOUCHER """
def disapproved(request):    
    if not request.user.user_type == 4:
        return HttpResponse('You are not allowed to view this page')
    else:

        user = User.objects.get(id=request.user.id)
        voucher = PaymentRequisitionVoucher.objects.filter(approved_by=2, acknowledge_by=2).filter(client__user=user).order_by('-voucher_updated_at')
        context = {
            'vouchers':voucher
        }
    return render(request,'voucher/total_disapprove.html',context)



""" SEARCH QUERY """
def search(request):    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            user = User.objects.get(id=request.user.id)
            voucher = PaymentRequisitionVoucher.objects.get(Q(tracking_id__iexact=keyword))
            # data = voucher
            # print(data.payee, data.requested_by)
            
        else:
            print('result not found')    
    # context = {
    #     'data':data
    # }        
                  
    return render(request,'voucher/search.html')


""" 
central ADMIN PAGE  """
def central_page(request):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        user = User.objects.all()        
        voucher = PaymentRequisitionVoucher.objects.all()
        form = UploadMemberForm()
        context = {
            'vouchers':voucher,
            'user':user,
            'form':form
        }    
        return render(request,'voucher/central_admin.html',context)

""" BULK UPLOAD OF MEMBER """
def bulk_upload_member(request):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        if request.method == 'POST':
            # user =User.objects.all().exists()
            form = UploadMemberForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                # if user:
                #     print('User already exists')
                #     print(user)
                    
                #     messages.error(request, 'User Already exists')
                #     return redirect('central_page')
                form.save()

                

                # get the upload model 
                obj_csv = UploadMember.objects.get(activated = False)

                # open the file to have access to each row 
                with open(obj_csv.file_name.path, 'r') as f:
                    reader = csv.reader(f)


                    for i, row in enumerate(reader):
                        if i == 0 :
                            pass
                        else:
                            row = " ".join(row)
                            row = row.replace(";", " ")
                            row = row.split()
                            print(row)
                            print(type(row))
                            email = row[0]
                            username = row[1]
                            password = row[2]
                            user_type = int(row[3])
                            print('email before :' + email)

                            # if User.objects.filter(email=user.email).exists():
                            #     User.objects.filter(email=user.email).delete()
                            #     print('email deleted')
                            # # else:                             
                            
                            user = User.objects.update_or_create(email=email,username=username,password=password,user_type=user_type)
                                                        
                            user.save()
                            
                            print(email, username, password)

                    obj_csv.activated = True
                    
                    # obj_csv.save(commit =False)
                    
                    obj_csv.save()    
                    print('success')        
                    messages.success(request, 'File Uploaded successfully and users has been created')
                    return redirect('central_page')
            else:
                form = UploadMemberForm()
            context = {
                'form':form
            }

        return render(request, 'voucher/central_admin.html',context)    











""" ACKNOWLEGE ADMIN PAGE """     
@login_required
def acknowlege(request):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
       
        voucher = PaymentRequisitionVoucher.objects.filter(client__user__user_type = 4)
       
        context = {
            'vouchers':voucher,

        } 
           
    return render(request,'voucher/acknowlege.html',context)


""" MANAGER ADMIN PAGE """     
@login_required
def manager_page(request):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:
        user = User.objects.get(id=request.user.id)
        voucher = PaymentRequisitionVoucher.objects.filter(client__user__user_type = 4)
        # print(request.user.email)
        context = {
            'vouchers':voucher,
            'user':user
        }    
    return render(request,'voucher/manager.html',context)


""" APPROVE voucher BY TEAM LEADER  """
def approve_team_leader(request, team_id):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        voucher = PaymentRequisitionVoucher.objects.get(id=team_id)    
        voucher.voucher_status_isteamleader = 1
        voucher.save()
        
        print('voucher approved')
        return redirect('table_voucher')


""" DISAPPROVE voucher BY TEAM LEADER  """
def disapprove_team_leader(request, team_id):
    if not request.user.user_type == 1:
        return HttpResponse('You are not allow to view this page')
    else:
        voucher = PaymentRequisitionVoucher.objects.get(id=team_id)    
        voucher.voucher_status_isteamleader = 2
        voucher.save()
        print('voucher approved')
        return redirect('table_voucher')



""" APPROVE voucher BY ACKNOWLEGE  """
def approve_acknowlege(request, acknowlege_id):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
        voucher = PaymentRequisitionVoucher.objects.get(id=acknowlege_id)    
        voucher.acknowledge_by = 1
        voucher.save()
        messages.success(request,'You have approve this request with tracking number ' + voucher.tracking_id )
        return redirect('acknowlege')


""" DISAPPROVE voucher BY ACKNOWLEGE  """
def disapprove_acknowlege(request, acknowlege_id):
    if not request.user.user_type == 2:
        return HttpResponse('You are not allow to view this page')
    else:
        voucher = PaymentRequisitionVoucher.objects.get(id=acknowlege_id)    
        voucher.acknowledge_by = 2
        voucher.save()
        messages.success(request,'You have disapprove this request with tracking number ' + voucher.tracking_id )       
        return redirect('acknowlege')


""" APPROVE voucher BY MANAGER  """
def approved_manager(request, manager_id):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:   
            
        voucher = PaymentRequisitionVoucher.objects.get(id=manager_id)    
        voucher.approved_by = 1
        voucher.save()

        email = voucher.client.user.email
        
        current_site = get_current_site(request)
        mail_subject = 'Finally Approved'
        
        html_message = render_to_string('voucher/email_approve_admin_text.html', {
            'domain':current_site,
            
            'voucher':voucher,            


        })
        to = email
        send_email = EmailMessage(mail_subject, html_message, to=[to])
        send_email.content_subtype = "html"
        send_email.send()
        
        messages.success(request,'You have approve this request with tracking number ' + voucher.tracking_id )
        return redirect('manager_page')
               

""" DISAPPROVE voucher BY MANAGER  """
def disapproved_manager(request, manager_id):
    if not request.user.user_type == 3:
        return HttpResponse('You are not allow to view this page')
    else:
        voucher = PaymentRequisitionVoucher.objects.get(id=manager_id)    
        voucher.approved_by = 2
        voucher.save()

        email = voucher.client.user.email
        
        current_site = get_current_site(request)
        mail_subject = 'Opps Disapprove'
        
        html_message = render_to_string('voucher/email_disapprove_admin_text.html', {
            'domain':current_site,            
            'voucher':voucher,          


        })
        to = email
        send_email = EmailMessage(mail_subject, html_message, to=[to])
        send_email.content_subtype = "html"
        send_email.send()
        messages.success(request,'You have disapprove this request with tracking number ' + voucher.tracking_id )
        return redirect('manager_page')
                              

""" PDF """                              
def print_approved(request, voucher_id):        
    voucher = PaymentRequisitionVoucher.objects.get(id=voucher_id)
    manager = manager_page(request)
    current_site = get_current_site(request)
    verify = PaymentVerification.objects.get(payvoucher=voucher_id)
    url = f'print_approve/{voucher_id}'
    verify.name = f'{current_site}/{url}/.com'
    verify.save()
    print(url)
    
    print('pdf')
    print(verify.name)
    print(verify.qr_code)
    verify.save()
    print(manager)   
    template_path = 'voucher/voucher_slip.html'
    context = {
        'voucher':voucher,
        'verify':verify
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename ="voucher_slip.pdf"'

    # get template to display it 
    template = get_template(template_path)
    html = template.render(context)

    # create pdf 
    pisa_create = pisa.CreatePDF( html,
    dest=response)
    if pisa_create.err:
        return HttpResponse('Error in displaying')
    return response


# DELETE EACH VOUCHER 
@login_required
def delete_voucher(request,voucher_id):
    voucher = PaymentRequisitionVoucher.objects.get(id=voucher_id)
    if request.method == 'POST':
        # voucher = PaymentRequisitionVoucher.objects.get(is_deleted=False)

        voucher.is_deleted = True
        voucher.save()
        print(voucher.payee)
        messages.success(request, 'You have successfully delete this voucher')
        return redirect('dashboard')
    
    context = {
        'voucher':voucher_id
    }    

    return render(request, 'voucher/delete_voucher.html',context)



def update_voucher_save(request):
    if not request.user.user_type == 4:
        return HttpResponse('You are not allow to view this page')    
    else:
        if request.method != 'POST':
            print('request not post')
            # return redirect('')
        else:
            voucher_id = request.POST['voucher_id']
            client = request.POST['client']
            payee = request.POST['payee']    
            account_number = request.POST['account_number']
            qty = request.POST['qty']
            rate = request.POST['rate']
            details = request.POST['details']
            amount = request.POST['amount']

            qty_2 = request.POST['qty_2']
            rate_2 = request.POST['rate_2']
            details_2 = request.POST['details_2']
            amount_2 = request.POST['amount_2']

            qty_3 = request.POST['qty_3']
            rate_3 = request.POST['rate_3']
            details_3 = request.POST['details_3']
            amount_3 = request.POST['amount_3']

            qty_4 = request.POST['qty_4']
            rate_4 = request.POST['rate_4']
            details_4 = request.POST['details_4']
            amount_4 = request.POST['amount_4']

            qty_5 = request.POST['qty_5']
            rate_5 = request.POST['rate_5']
            details_5 = request.POST['details_5']
            amount_5 = request.POST['amount_5']

            total = request.POST['total']
            amount_in_words = request.POST['amount_in_words']
            requested_by = request.POST['requested_by']
            acknowlege_email = request.POST['acknowlege_email']
            approve_email = request.POST.get('approve_email')
            print('Before DB: ' + acknowlege_email)
            # try:
            # user = User.objects.get(id=voucher_id)
            # user.email = client
            # user.save()

            client_obj = Client.objects.get(user=request.user.id)
            client_obj.user.email = client

            client_obj.save()

            voucher = PaymentRequisitionVoucher.objects.get(id=voucher_id)

            payverify = PaymentVerification.objects.get(id=voucher_id)

            current_site = get_current_site(request)
            url = f'voucher/{voucher_id}/update/'
            payverify.name = f'{current_site}/{url}.com'
            payverify.save()
            print(payverify.name)

            
            
            voucher.client = client_obj
            voucher.payee = payee
            voucher.account_number = account_number

            voucher.qty = qty
            voucher.rate = rate
            voucher.details = details
            voucher.amount = amount

            voucher.qty_2 = qty_2
            voucher.rate_2 = rate_2
            voucher.details_2 = details_2
            voucher.amount_2 = amount_2

            voucher.qty_3 = qty_3
            voucher.rate_3 = rate_3
            voucher.details_3 = details_3
            voucher.amount_3 = amount_3

            voucher.qty_4 = qty_4
            voucher.rate_4 = rate_4
            voucher.details_4 = details_4
            voucher.amount_4 = amount_4

            voucher.qty_5 = qty_5
            voucher.rate_5 = rate_5
            voucher.details_5 = details_5
            voucher.amount_5 = amount_5

            voucher.total = total
            voucher.amount_in_words = amount_in_words
            voucher.requested_by = requested_by
            
            # voucher.approve_email = approve_email

            if voucher.approve_email != approve_email:

                # SEND EMAIL FOR UPDATING EMAIL  
                current_site = get_current_site(request)
                mail_subject = 'Approvement Recall'
                
                html_message = render_to_string('voucher/email/new_recall_approve_text.html', {
                    'approve_email': voucher.approve_email,
                    'acknowlege_email':acknowlege_email,            
                    'voucher':voucher,            
                    'domain':current_site,
                })
                to = voucher.approve_email
                send_email = EmailMessage(mail_subject, html_message, to=[to])
                send_email.content_subtype = "html"
                send_email.send()
                print(approve_email)
                voucher.approve_email = approve_email

                # SEND EMAIL FOR UPDATING EMAIL  
                current_site = get_current_site(request)
                mail_subject = 'New Assign For Approvement'
                
                html_message = render_to_string('voucher/email/new_assign_approve_text.html', {
                    'approve_email': voucher.approve_email,
                    'acknowlege_email':acknowlege_email,            
                    'voucher':voucher,            
                    'domain':current_site,
                })
                to = voucher.approve_email
                send_email = EmailMessage(mail_subject, html_message, to=[to])
                send_email.content_subtype = "html"
                send_email.send()
                print(approve_email)
                

            if voucher.acknowlege_email != acknowlege_email:

                # SEND EMAIL FOR UPDATING EMAIL  
                current_site = get_current_site(request)
                mail_subject = 'Acknowlegement Recall'
                
                html_message = render_to_string('voucher/email/new_recall_email_text.html', {
                    'acknowlege_email': voucher.acknowlege_email,
                    'approve_email':approve_email,            
                    'voucher':voucher,            
                    'domain':current_site,
                })
                to = voucher.acknowlege_email
                send_email = EmailMessage(mail_subject, html_message, to=[to])
                send_email.content_subtype = "html"
                send_email.send()
                print(acknowlege_email)
                voucher.acknowlege_email = acknowlege_email
                

                # SEND EMAIL FOR UPDATING EMAIL  
                current_site = get_current_site(request)
                mail_subject = 'New Assign For Acknowlegement'
                
                html_message = render_to_string('voucher/email/new_assign_email_text.html', {
                    'acknowlege_email': voucher.acknowlege_email,
                    'approve_email':approve_email,            
                    'voucher':voucher,            
                    'domain':current_site,
                })
                to = voucher.acknowlege_email
                send_email = EmailMessage(mail_subject, html_message, to=[to])
                send_email.content_subtype = "html"
                send_email.send()
                print(acknowlege_email)
            else:
                print(voucher.acknowlege_email)
         
            
            messages.success(request, 'Voucher updated successfully')
            voucher.save()
            payverify.save()
            return redirect('dashboard')
             
        return render(request, 'voucher/update_voucher.html') 


def update_voucher(request,voucher_id):
    if not request.user.user_type ==4 :
        return HttpResponse('You are not allow to view this page')
    else:
        payverify = PaymentVerification.objects.get(payvoucher=voucher_id)
        current_site = get_current_site(request)        
        url = f'voucher/{voucher_id}/update/' 
        payverify.name = f'{current_site}/{url}.com'
        payverify.save()
        print(payverify.name)
        voucher = PaymentRequisitionVoucher.objects.get(id=voucher_id)
        acknowlege_email = request.POST.get('acknowlege_email')

        if voucher.acknowlege_email != acknowlege_email:
            print( voucher.acknowlege_email)

        context = {
            'voucher':voucher,
            'id':voucher_id,
            'payverify':payverify,
           
        }

        return render(request, 'voucher/update_voucher.html',context)