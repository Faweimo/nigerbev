from django.contrib import admin
from .models import PaymentRequisitionVoucher, PaymentVerification, UploadMember,Tested
from django.urls import path
from django.shortcuts import render


class PaymentRequisitionVoucherAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'payee')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/',self.upload_csv)]
        return new_urls + urls

    def upload_csv(self,request):    
        return render(request,'admin/csv_upload.html')
admin.site.register(PaymentRequisitionVoucher)


admin.site.register(UploadMember)
admin.site.register(PaymentVerification)
