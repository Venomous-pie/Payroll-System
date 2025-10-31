from django.urls import path
from . import views

urlpatterns = [

    path('onboarding/', views.onboarding_queue, name='staff_onboarding'),
    

    path('leave-calendar/', views.leave_calendar, name='staff_leave_calendar'),
    

    path('attendance-summary/', views.attendance_summary, name='staff_attendance_summary'),
    

    path('bank-transfers/', views.bank_transfers, name='staff_bank_transfers'),
    path('deposit-status/', views.deposit_status, name='staff_deposit_status'),
    

    path('performance/', views.performance_reviews, name='staff_performance'),
    path('benefits/', views.benefits_management, name='staff_benefits'),
    

    path('analytics/', views.hr_analytics, name='staff_analytics'),
    

    path('settings/', views.hr_settings, name='staff_settings'),
    path('audit-logs/', views.audit_logs, name='staff_audit_logs'),
]
