from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    path('salary-grades/', views.salarygrade_list, name='salarygrade_list'),
    path('salary-grades/create/', views.salarygrade_create, name='salarygrade_create'),
    path('salary-grades/<int:pk>/edit/', views.salarygrade_update, name='salarygrade_update'),
    

    path('my/salary-info/', views.my_salary_info, name='my_salary_info'),
]
