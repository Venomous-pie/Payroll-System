from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max
from accounts.decorators import group_required
from .models import Employee, SalaryGrade
from .forms import EmployeeForm, SalaryGradeForm

@login_required
@group_required('Staff')
def employee_list(request):
    employees = Employee.objects.select_related('salary_grade', 'user').all()
    active_count = employees.filter(active=True).count()
    
    context = {
        'employees': employees,
        'active_count': active_count,
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
@group_required('Staff')
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Create Employee'})

@login_required
@group_required('Staff')
def employee_update(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=obj)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Update Employee'})

@login_required
@group_required('Staff')
def employee_delete(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'object': obj, 'type': 'Employee'})

@login_required
@group_required('Staff')
def salarygrade_list(request):
    grades = SalaryGrade.objects.all()
    
    # Calculate stats for widgets
    min_pay = grades.aggregate(Min('base_pay'))['base_pay__min'] if grades.exists() else 0
    max_pay = grades.aggregate(Max('base_pay'))['base_pay__max'] if grades.exists() else 0
    steps_count = grades.values('step').distinct().count()
    
    context = {
        'grades': grades,
        'min_pay': min_pay,
        'max_pay': max_pay,
        'steps_count': steps_count,
    }
    return render(request, 'employees/salarygrade_list.html', context)

@login_required
@group_required('Staff')
def salarygrade_create(request):
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salarygrade_list')
    else:
        form = SalaryGradeForm()
    return render(request, 'employees/salarygrade_form.html', {'form': form, 'title': 'Create Salary Grade'})

@login_required
@group_required('Staff')
def salarygrade_update(request, pk):
    obj = get_object_or_404(SalaryGrade, pk=pk)
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('salarygrade_list')
    else:
        form = SalaryGradeForm(instance=obj)
    return render(request, 'employees/salarygrade_form.html', {'form': form, 'title': 'Update Salary Grade'})

@login_required
def my_salary_info(request):
    """Employee view of their own salary information"""
    try:
        employee = request.user.employee
        return render(request, 'employees/my_salary_info.html', {'employee': employee})
    except Employee.DoesNotExist:
        return render(request, 'employees/my_salary_info.html', {
            'employee': None,
            'error': 'No employee record found for your account. Please contact HR.'
        })
