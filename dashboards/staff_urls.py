from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.staff_dashboard, name='staff_dashboard'),
    

    path('', include('staff.urls')),
]
