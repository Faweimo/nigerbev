from .import views
from django.urls import path
# from .import pdf
urlpatterns = [
    path('request', views.index, name='index'),
    path('', views.home, name='home'),
    path('table_leave',views.table_leave,name='table_leave'),
    path('approve_team_leader/<int:team_id>/approved',views.approve_team_leader,name='approve_team_leader'),
    path('disapprove_team_leader/<int:team_id/disapproved',views.disapprove_team_leader,name='disapprove_team_leader'),
    path('approve_supose/<int:supose_id>/approved',views.approve_supose,name='approve_supose'),
    path('disapprove_supose/<int:supose_id>/disapproved',views.disapprove_supose,name='disapprove_supose'),
    path('approve_manager/<int:manager_id>/approved',views.approve_manager,name='approve_manager'),
    path('disapprove_manager/<int:manager_id>/disapproved',views.disapprove_manager,name='disapprove_manager'),


    path('team_leader_page',views.team_leader_page,name='team_leader_page'),
    path('supevisor_leader_page',views.supevisor_leader_page,name='supevisor_leader_page'),
    path('manager_leader_page',views.manager_leader_page,name='manager_leader_page'),

    path('staff_request_pdf/<int:leave_id>/',views.staff_request_pdf,name='staff_request_pdf')
]