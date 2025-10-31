from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.decorators import group_required
from employees.models import Employee, SalaryGrade
from attendance.models import AttendanceLog, LeaveRequest
from payroll.models import PayrollRun, Payslip, Loan, OtherDeduction


@login_required
@group_required('Staff')
def onboarding_queue(request):
    """Manage new employee onboarding process"""

    recent_employees = Employee.objects.filter(
        date_hired__gte=timezone.now().date() - timedelta(days=30)
    ).select_related('user', 'salary_grade').order_by('-date_hired')
    

    incomplete_bank_info = Employee.objects.filter(
        Q(bank_name__isnull=True) | Q(bank_name='') | 
        Q(bank_account__isnull=True) | Q(bank_account='')
    ).select_related('user')
    
    return render(request, 'staff/onboarding_queue.html', {
        'recent_employees': recent_employees,
        'incomplete_bank_info': incomplete_bank_info,
    })


@login_required
@group_required('Staff')
def leave_calendar(request):
    """View leave calendar and upcoming leaves"""

    current_month = timezone.now().date().replace(day=1)
    next_month = (current_month + timedelta(days=32)).replace(day=1)
    
    approved_leaves = LeaveRequest.objects.filter(
        status='APPROVED',
        start_date__gte=current_month,
        start_date__lt=next_month
    ).select_related('employee').order_by('start_date')
    

    pending_leaves = LeaveRequest.objects.filter(
        status='PENDING'
    ).select_related('employee').order_by('created_at')
    
    return render(request, 'staff/leave_calendar.html', {
        'approved_leaves': approved_leaves,
        'pending_leaves': pending_leaves,
        'current_month': current_month,
    })


@login_required
@group_required('Staff')
def attendance_summary(request):
    """Generate attendance summary and reports"""

    current_month = timezone.now().date().replace(day=1)
    

    total_employees = Employee.objects.filter(active=True).count()
    attendance_records = AttendanceLog.objects.filter(
        date__gte=current_month
    ).select_related('employee')
    

    present_today = AttendanceLog.objects.filter(
        date=timezone.now().date(),
        time_in__isnull=False
    ).count()
    
    absent_today = total_employees - present_today
    

    late_today = AttendanceLog.objects.filter(
        date=timezone.now().date(),
        time_in__gt='09:00:00'
    ).count()
    
    return render(request, 'staff/attendance_summary.html', {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'late_today': late_today,
        'attendance_records': attendance_records[:50],  # Recent 50 records
    })


@login_required
@group_required('Staff')
def bank_transfers(request):
    """Manage bank transfers and salary deposits"""

    payroll_runs = PayrollRun.objects.all().order_by('-created_at')[:10]
    

    recent_payslips = Payslip.objects.select_related(
        'employee', 'payroll_run'
    ).order_by('-payroll_run__created_at')[:100]
    

    total_pending = Payslip.objects.filter(
        bank_file_generated=False
    ).count()
    
    total_generated = Payslip.objects.filter(
        bank_file_generated=True,
        salary_deposited=False
    ).count()
    
    total_deposited = Payslip.objects.filter(
        salary_deposited=True
    ).count()
    
    return render(request, 'staff/bank_transfers.html', {
        'payroll_runs': payroll_runs,
        'recent_payslips': recent_payslips,
        'total_pending': total_pending,
        'total_generated': total_generated,
        'total_deposited': total_deposited,
    })

@login_required
@group_required('Staff')
def deposit_status(request):
    """View detailed deposit status for all employees"""

    employees_with_deposits = Employee.objects.filter(
        active=True
    ).select_related('user').prefetch_related('payslip_set')
    
    return render(request, 'staff/deposit_status.html', {
        'employees_with_deposits': employees_with_deposits,
    })


@login_required
@group_required('Staff')
def performance_reviews(request):
    """Manage employee performance reviews"""
    employees = Employee.objects.filter(active=True).select_related('user', 'salary_grade')
    

    for employee in employees:
        if employee.date_hired:
            employee.tenure_days = (timezone.now().date() - employee.date_hired).days
            employee.tenure_years = employee.tenure_days / 365.25
        else:
            employee.tenure_days = 0
            employee.tenure_years = 0
    
    return render(request, 'staff/performance_reviews.html', {
        'employees': employees,
    })

@login_required
@group_required('Staff')
def benefits_management(request):
    """Manage employee benefits and deductions"""

    active_loans = Loan.objects.filter(is_active=True).select_related('employee')
    active_deductions = OtherDeduction.objects.filter(is_active=True).select_related('employee')
    

    total_loan_amount = active_loans.aggregate(
        total=Sum('remaining_balance')
    )['total'] or 0
    
    total_monthly_deductions = active_loans.aggregate(
        total=Sum('monthly_deduction')
    )['total'] or 0
    
    total_other_deductions = active_deductions.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    return render(request, 'staff/benefits_management.html', {
        'active_loans': active_loans,
        'active_deductions': active_deductions,
        'total_loan_amount': total_loan_amount,
        'total_monthly_deductions': total_monthly_deductions,
        'total_other_deductions': total_other_deductions,
    })


@login_required
@group_required('Staff')
def hr_analytics(request):
    """Generate HR analytics and insights"""

    total_employees = Employee.objects.filter(active=True).count()
    inactive_employees = Employee.objects.filter(active=False).count()
    

    department_stats = Employee.objects.filter(active=True).values(
        'department'
    ).annotate(count=Count('id')).order_by('-count')
    

    position_stats = Employee.objects.filter(active=True).values(
        'position'
    ).annotate(count=Count('id')).order_by('-count')
    

    salary_grade_stats = Employee.objects.filter(active=True).values(
        'salary_grade__code'
    ).annotate(count=Count('id')).order_by('salary_grade__code')
    

    six_months_ago = timezone.now().date() - timedelta(days=180)
    recent_hires = Employee.objects.filter(
        date_hired__gte=six_months_ago
    ).count()
    

    current_year = timezone.now().year
    leave_stats = LeaveRequest.objects.filter(
        created_at__year=current_year
    ).values('status').annotate(count=Count('id'))
    
    return render(request, 'staff/hr_analytics.html', {
        'total_employees': total_employees,
        'inactive_employees': inactive_employees,
        'department_stats': department_stats,
        'position_stats': position_stats,
        'salary_grade_stats': salary_grade_stats,
        'recent_hires': recent_hires,
        'leave_stats': leave_stats,
    })


@login_required
@group_required('Staff')
def hr_settings(request):
    """HR system settings and configuration"""

    total_payroll_runs = PayrollRun.objects.count()
    total_payslips = Payslip.objects.count()
    total_leave_requests = LeaveRequest.objects.count()
    

    salary_grades = SalaryGrade.objects.all().order_by('code', 'step')
    
    return render(request, 'staff/hr_settings.html', {
        'total_payroll_runs': total_payroll_runs,
        'total_payslips': total_payslips,
        'total_leave_requests': total_leave_requests,
        'salary_grades': salary_grades,
    })

@login_required
@group_required('Staff')
def audit_logs(request):
    """View system audit logs"""
    try:
        from accounts.models import AuditLog

        logs = AuditLog.objects.select_related('user').order_by('-created_at')[:100]
    except ImportError:

        logs = []
    
    return render(request, 'staff/audit_logs.html', {
        'logs': logs,
    })
