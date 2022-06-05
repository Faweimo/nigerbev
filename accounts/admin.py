from asyncore import file_dispatcher
from pyexpat.errors import messages
from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import User, Client
from django.urls import path, reverse
from   django.shortcuts import render
from django import forms
import csv


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/',self.upload_csv)]
        return new_urls + urls

    def upload_csv(self,request):  

        if request.method =='POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request,'Upload file that end with .csv format')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split('\n')

            for x in csv_data:
                fields = x.split(",")
               
            
                create = User.objects.update_or_create(email = fields[0],username = fields[1],password = fields[2],user_type=fields[3])

            url = reverse('admin:index')
            return HttpResponseRedirect(url)
                    

        form = CsvImportForm()
        data = {'form':form}  
        return render(request,'admin/csv_upload.html',data)
admin.site.register(User,UserAdmin)
admin.site.register(Client)
