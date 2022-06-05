from django import forms
from .models import PaymentRequisitionVoucher, Tested, UploadMember
# from django.utils.translation import gettext_lazy as _


# form bulk creations of member
class UploadMemberForm(forms.ModelForm):
    class Meta:
        model = UploadMember
        fields = ("file_name",)

class PaymentRequisitionForm(forms.ModelForm):
    
    class Meta:
        model = PaymentRequisitionVoucher
        fields = '__all__'
        exclude = 'tracking_id','acknowledge_by','approved_by',


class UpdatePaymentRequisitionForm(forms.ModelForm):
    class Meta:
        model = PaymentRequisitionVoucher
        fields = '__all__'
        exclude = 'acknowledge_by','approved_by',
        # widgets = {
        #     'client':forms.TextInput(attrs={
        #         'type':'hidden',
        #     }),
            
        # }    

class TestingForm(forms.ModelForm):
    class Meta:
        model = Tested
        fields ='__all__'
        exclude = ('user',)
