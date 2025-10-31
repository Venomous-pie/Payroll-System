from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from accounts.decorators import group_required
from .models import AttendanceLog, LeaveRequest
from .forms import AttendanceLogForm, LeaveRequestForm
from employees.models import Employee

@login_required
@group_required('Staff')
def attendance_list(request):
    from datetime import date, time
    
    # Get all logs (limited to 200 for display)
    logs = AttendanceLog.objects.select_related('employee').all()[:200]
    
    # Get all logs for today (no limit for stats)
    today = date.today()
    today_logs = AttendanceLog.objects.filter(date=today)
    
    # Calculate statistics for today
    present_today = today_logs.filter(time_in__isnull=False).count()
    absent_today = Employee.objects.filter(active=True).count() - present_today
    
    # Calculate late arrivals (arrived after 9:00 AM)
    late_time = time(9, 0)  # 9:00 AM
    late_count = today_logs.filter(time_in__gt=late_time).count()
    
    context = {
        'logs': logs,
        'present_today': present_today,
        'absent_today': absent_today,
        'late_count': late_count,
    }
    return render(request, 'attendance/attendance_list.html', context)

@login_required
@group_required('Staff')
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceLogForm()
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Create Attendance Log'})

@login_required
def leave_submit(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:

        return render(request, 'attendance/leave_form.html', {
            'form': None, 
            'title': 'Submit Leave Request',
            'error': 'No employee record found for your account. Please contact HR.'
        })
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            lr = form.save(commit=False)
            lr.employee = employee
            lr.save()
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'attendance/leave_form.html', {'form': form, 'title': 'Submit Leave Request'})

@login_required
@group_required('Staff')
def leave_queue(request):
    # Get base queryset without slicing first
    all_leaves = LeaveRequest.objects.select_related('employee').order_by('-created_at')
    
    # Calculate status counts from base queryset
    pending_count = all_leaves.filter(status='PENDING').count()
    approved_count = all_leaves.filter(status='APPROVED').count()
    rejected_count = all_leaves.filter(status='REJECTED').count()
    
    # Now slice for display
    leaves = all_leaves[:200]
    
    context = {
        'leaves': leaves,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'attendance/leave_queue.html', context)

@login_required
@group_required('Staff')
def leave_decide(request, pk, decision):
    lr = get_object_or_404(LeaveRequest, pk=pk)
    if decision.upper() in ['APPROVED', 'REJECTED']:
        lr.status = decision.upper()
        lr.decided_by = request.user
        lr.decided_at = timezone.now()
        lr.save()
    return redirect('leave_queue')

@login_required
def my_leave_history(request):
    """Employee view of their own leave requests"""
    try:
        employee = request.user.employee
        leaves = LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
    except Employee.DoesNotExist:
        leaves = []
    
    return render(request, 'attendance/my_leave_history.html', {'leaves': leaves})

@login_required
def my_attendance_records(request):
    """Employee view of their own attendance records"""
    try:
        employee = request.user.employee
        records = AttendanceLog.objects.filter(employee=employee).order_by('-date')[:30]  # Last 30 records
    except Employee.DoesNotExist:
        records = []
    
    return render(request, 'attendance/my_attendance_records.html', {'records': records})
