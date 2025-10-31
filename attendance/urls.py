from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('create/', views.attendance_create, name='attendance_create'),
    path('leaves/', views.leave_queue, name='leave_queue'),
    path('leaves/submit/', views.leave_submit, name='leave_submit'),
    path('leaves/<int:pk>/<str:decision>/', views.leave_decide, name='leave_decide'),

    path('my/leaves/', views.my_leave_history, name='my_leave_history'),
    path('my/records/', views.my_attendance_records, name='my_attendance_records'),
]
