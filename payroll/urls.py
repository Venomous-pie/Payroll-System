from django.urls import path
from . import views

urlpatterns = [
    # Staff/HR views
    path('runs/', views.run_list, name='payroll_run_list'),
    path('runs/create/', views.run_create, name='payroll_run_create'),
    path('runs/<int:run_id>/payslips/', views.run_payslips, name='payroll_run_payslips'),
    path('runs/<int:run_id>/edit/', views.edit_payroll_run, name='edit_payroll_run'),
    path('runs/<int:run_id>/recalculate/', views.recalculate_payslips, name='recalculate_payslips'),
    path('runs/<int:run_id>/status/', views.update_payroll_status, name='update_payroll_status'),
    path('runs/<int:run_id>/generate-pdfs/', views.generate_all_payslip_pdfs, name='generate_all_pdfs'),
    path('runs/<int:run_id>/export-excel/', views.export_payroll_excel, name='export_payroll_excel'),
    path('runs/<int:run_id>/generate-bank-file/', views.generate_bank_transfer_file, name='generate_bank_file'),
    path('runs/<int:run_id>/mark-deposited/', views.mark_salaries_deposited, name='mark_salaries_deposited'),
    
    # Employee self-service
    path('my/payslips/', views.my_payslips, name='my_payslips'),
    path('my/payslips/<int:slip_id>/', views.my_payslip_detail, name='my_payslip_detail'),
    path('my/payslips/<int:slip_id>/download-pdf/', views.download_payslip_pdf, name='download_payslip_pdf'),
    path('my/deposits/', views.my_deposit_status, name='my_deposit_status'),
    
    # Loan and deduction management
    path('loans/', views.loan_management, name='loan_management'),
    path('deductions/', views.deduction_management, name='deduction_management'),
]
