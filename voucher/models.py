from django.db import models
from accounts.models import Client, User
import random

from approval.models import Approve
from .utils import client_uid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class PaymentRequisitionVoucher(models.Model):
    client              = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    tracking_id         = models.CharField(max_length=20,default=client_uid(),editable=False)
    payee               = models.CharField(max_length=250)
    account_number      = models.CharField(max_length=250)

    qty                 = models.CharField(max_length=250)
    rate                = models.CharField(max_length=250)
    details             = models.CharField(max_length=250)
    amount              = models.CharField(max_length=250)

    qty_2                 = models.CharField(max_length=250,blank=True,null=True)
    rate_2                = models.CharField(max_length=250,blank=True,null=True)
    details_2             = models.CharField(max_length=250,blank=True,null=True)
    amount_2              = models.CharField(max_length=250,blank=True,null=True)

    qty_3                 = models.CharField(max_length=250,blank=True,null=True)
    rate_3                = models.CharField(max_length=250,blank=True,null=True)
    details_3             = models.CharField(max_length=250,blank=True,null=True)
    amount_3              = models.CharField(max_length=250,blank=True,null=True)

    qty_4                 = models.CharField(max_length=250,blank=True,null=True)
    rate_4                = models.CharField(max_length=250,blank=True,null=True)
    details_4             = models.CharField(max_length=250,blank=True,null=True)
    amount_4             = models.CharField(max_length=250,blank=True,null=True)

    qty_5                 = models.CharField(max_length=250,blank=True,null=True)
    rate_5                = models.CharField(max_length=250,blank=True,null=True)
    details_5             = models.CharField(max_length=250,blank=True,null=True)
    amount_5             = models.CharField(max_length=250,blank=True,null=True)

    total               = models.CharField(max_length=250)
    amount_in_words     = models.CharField(max_length=250)
    requested_by        = models.CharField(max_length=250)
    acknowledge_by      = models.IntegerField(default=0)
    approved_by         = models.IntegerField(default=0)
    voucher_created_at  = models.DateTimeField(auto_now_add=True)
    voucher_updated_at  = models.DateField(auto_now=True)

    acknowlege_email = models.EmailField(blank=True,null=True)
    approve_email = models.EmailField(blank=True,null=True)

    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.tracking_id} - {self.requested_by}'

    class Meta:        
        verbose_name = 'Payment Requisition Voucher'
        verbose_name_plural = 'Payment Requisition Vouchers'
        ordering = ('-voucher_updated_at',)

    """ 
    Generating Tracking ID for each Voucher
    """    
    # def save(self, *args,**kw):
    #     tracking_id_list = [x for x in range(10)]
    #     tracking_items = ['NBL']

    #     for i in range(6):
    #         num = random.choice(tracking_id_list)
    #         tracking_items.append(num)

    #     tracking_string = "".join(str(item) for item in tracking_items)    
    #     self.tracking_id = tracking_string
        
    #     super(PaymentRequisitionVoucher,self).save(*args,**kw)


class PaymentVerification(models.Model):
    payvoucher = models.ForeignKey(PaymentRequisitionVoucher, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    qr_code = models.ImageField(upload_to='qr_codes',blank=True)

    def __str__(self):
        return f'{self.id} - {self.payvoucher.tracking_id}'

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)    
        canvas = Image.new('RGB', (290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname,File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class UploadMember(models.Model):
    
    file_name                   = models.FileField(upload_to='membercreation')
    activated                     = models.BooleanField(default=False)
    created_at                    = models.DateField(auto_now_add=True)
    updated_at                    = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ("Bulk Creation")
        verbose_name_plural = ("Bulk Creations")    


class Tested(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    approved_by = models.ForeignKey(Approve,on_delete=models.PROTECT)
    acknownlege_by = models.ForeignKey(User,on_delete=models.PROTECT,related_name='acknowlege')
    mtext = models.TextField()

    def __str__(self):
        return self.id