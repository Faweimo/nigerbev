import imp
from unicodedata import name
from django import views
from django.urls import path
from .import views

urlpatterns = [
    path('',views.search,name='search'),
    path('request/voucher/',views.requestclient,name='requestclient'),
    path('request/voucher/save',views.requestclient_save,name='requestclient_save'),
    # path('success_page/',views.success_page,name='success_page'),
    path('voucher/<int:voucher_id>/update/',views.update_voucher,name='update'),
    path('voucher/update/save/',views.update_voucher_save,name='update_voucher_save'),

    path('voucher/<int:voucher_id>/delete/',views.delete_voucher,name='delete_voucher'),

    path('total_approved/',views.total_approved,name='total_approved'),
    path('pending_approved/',views.pending_approved,name='pending_approved'),
    path('disapproved/',views.disapproved,name='disapproved'),


    path('central_page/',views.central_page,name='central_page'),
    path('upload-file/',views.bulk_upload_member,name='bulk_upload_member'),
    # path('acknowlegement/<int:acknowlege_id>/disapproved',views.disapprove_acknowlege,name='disapprove_acknowlege'),

    path('acknowlegement/',views.acknowlege,name='acknowlege'),
    path('acknowlegement/<int:acknowlege_id>/approved',views.approve_acknowlege,name='approve_acknowlege'),
    path('acknowlegement/<int:acknowlege_id>/disapproved',views.disapprove_acknowlege,name='disapprove_acknowlege'),

    path('acknowlegement/manager/',views.manager_page,name='manager_page'),
    path('manager/<int:manager_id>/approved',views.approved_manager,name='approved_manager'),
    path('manager/<int:manager_id>/disapproved',views.disapproved_manager,name='disapproved_manager'),

    # pdf 
    path('print_approved/<int:voucher_id>/',views.print_approved,name='print_approved'),

    path('testing_page/',views.testing_page,name='testing_page'),
    path('testing_save/',views.testing_save,name='testing_save'),

]