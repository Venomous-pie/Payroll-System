from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports_index'),
    path('bir/', views.bir_summary, name='reports_bir'),
    path('gsis/', views.gsis_summary, name='reports_gsis'),
    path('export/<str:kind>/', views.export_csv, name='reports_export'),
]
