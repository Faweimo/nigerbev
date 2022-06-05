from django.shortcuts import render

from accounts.models import Client
from acknowledgement.forms import DemoForm
from acknowledgement.models import Acknlowledge
from voucher.models import PaymentRequisitionVoucher

def acknowledge_page(request):
    client = Client.objects.get(user=request.user.id)
    if request.method != 'POST':
        # description = request.POST['description']
        # acknowlege_by = request.POST['acknowlege_by']
        # approved_by = request.POST['approved_by']
        # ack = Acknlowledge.objects.get(id=)
        # payment = PaymentRequisitionVoucher.objects.create(client=client_obj,description=description)

        form = DemoForm()
    else:    
        form = DemoForm(request.POST or None)
        if form.is_valid():
            form.save()
            print('success')
        else:
            print('bad')
    form = DemoForm()
  
    return render(request,'acknowledgement/index.html',{'form':form, 'client':client})