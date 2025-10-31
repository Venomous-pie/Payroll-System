"""Quick script to delete all payroll data and re-seed"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from payroll.models import PayrollRun, Payslip, Loan, OtherDeduction
from attendance.models import AttendanceLog, LeaveRequest

print("Deleting all payroll data...")
PayrollRun.objects.all().delete()
Payslip.objects.all().delete()

print("Deleted payroll runs and payslips")
print("\nNow run: python manage.py seed_complete_system --months 14")
