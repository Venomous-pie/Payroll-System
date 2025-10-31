from datetime import date
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django import forms
from accounts.decorators import group_required
from .models import PayrollRun, Payslip, Loan, OtherDeduction
from .services import PayrollCalculator, update_loan_balances
from .pdf_generator import generate_payslip_pdf
from .bank_export import BankFileExporter, export_to_excel
from employees.models import Employee

class PayrollRunForm(forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['period_start', 'period_end']
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
        }

@login_required
@group_required('Staff')
def run_list(request):
    runs = PayrollRun.objects.all().order_by('-created_at')
    
    # Calculate status counts
    review_count = runs.filter(status='REVIEW').count()
    approved_count = runs.filter(status='APPROVED').count()
    paid_count = runs.filter(status='PAID').count()
    
    context = {
        'runs': runs,
        'review_count': review_count,
        'approved_count': approved_count,
        'paid_count': paid_count,
    }
    return render(request, 'payroll/run_list.html', context)

@login_required
@group_required('Staff')
def run_create(request):
    """Create new payroll run with automated calculations"""
    if request.method == 'POST':
        form = PayrollRunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            run.created_by = request.user
            run.status = 'DRAFT'
            run.save()

            # Calculate payslips for all active employees using new engine
            employees = Employee.objects.filter(active=True).select_related('salary_grade')
            payslips_created = 0
            
            for emp in employees:
                try:
                    # Use new PayrollCalculator
                    calculator = PayrollCalculator(
                        employee=emp,
                        period_start=run.period_start,
                        period_end=run.period_end
                    )
                    
                    payroll_data = calculator.compute_payslip()
                    
                    Payslip.objects.create(
                        payroll_run=run,
                        employee=emp,
                        **payroll_data
                    )
                    payslips_created += 1
                except Exception as e:
                    messages.warning(request, f"Could not calculate payroll for {emp}: {str(e)}")
            
            messages.success(request, f"Payroll run created successfully! {payslips_created} payslips generated.")
            return redirect('payroll_run_payslips', run_id=run.id)
    else:
        form = PayrollRunForm()
    return render(request, 'payroll/run_create.html', {'form': form})

@login_required
@group_required('Staff')
def run_payslips(request, run_id):
    from django.db.models import Sum
    
    run = get_object_or_404(PayrollRun, pk=run_id)
    slips = run.payslips.select_related('employee').all()
    
    # Calculate totals
    totals = slips.aggregate(
        total_gross=Sum('gross_pay'),
        total_sss=Sum('sss'),
        total_philhealth=Sum('philhealth'),
        total_pagibig=Sum('pagibig'),
        total_tax=Sum('tax'),
        total_net=Sum('net_pay')
    )
    
    return render(request, 'payroll/run_payslips.html', {
        'run': run, 
        'slips': slips,
        'totals': totals
    })

@login_required
def my_payslips(request):

    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        return render(request, 'payroll/my_payslips.html', {'slips': []})
    slips = Payslip.objects.filter(employee=emp).select_related('payroll_run').order_by('-payroll_run__created_at')
    return render(request, 'payroll/my_payslips.html', {'slips': slips})

@login_required
def my_payslip_detail(request, slip_id):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        emp = None
    slip = get_object_or_404(Payslip, pk=slip_id, employee=emp)
    return render(request, 'payroll/my_payslip_detail.html', {'slip': slip})

@login_required
@group_required('Staff')
def generate_bank_transfer_file(request, run_id):
    """Generate bank transfer CSV file"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    exporter = BankFileExporter(run)
    csv_content = exporter.generate_csv()
    exporter.mark_as_generated()
    
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="bank_transfer_{run.id}.csv"'
    
    messages.success(request, "Bank transfer file generated successfully!")
    return response

@login_required
@group_required('Staff')
def mark_salaries_deposited(request, run_id):
    """Step 9: Mark salaries as deposited to employee accounts"""
    from django.utils import timezone
    
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    # Prevent duplicate processing
    if run.status == 'PAID':
        messages.warning(request, "This payroll run has already been marked as PAID.")
        return redirect('payroll_run_payslips', run_id=run.id)
    
    if request.method == 'POST':
        # Update payslips that haven't been deposited yet
        payslips_to_update = run.payslips.filter(salary_deposited=False)
        payslips_to_update.update(
            salary_deposited=True,
            deposit_date=timezone.now()
        )
        
        # Update payroll run status to PAID
        run.status = 'PAID'
        run.paid_date = timezone.now()
        run.save()
        
        # Update loan balances only for payslips that weren't previously deposited
        for payslip in payslips_to_update:
            if payslip.loan_deductions > 0:
                # Find active loans for this employee
                loans = Loan.objects.filter(employee=payslip.employee, is_active=True)
                for loan in loans:
                    # Deduct the payment from remaining balance
                    loan.remaining_balance -= payslip.loan_deductions
                    if loan.remaining_balance <= 0:
                        loan.remaining_balance = 0
                        loan.is_active = False
                    loan.save()
        
        messages.success(request, f"Payroll run marked as PAID. Salaries deposited and loan balances updated.")
        return redirect('payroll_run_payslips', run_id=run.id)
    
    return render(request, 'payroll/confirm_deposit.html', {'run': run})

@login_required
@group_required('Staff')
def loan_management(request):
    """Manage employee loans"""
    loans = Loan.objects.select_related('employee').filter(is_active=True)
    
    # Calculate totals
    total_principal = sum(loan.principal_amount for loan in loans)
    total_outstanding = sum(loan.remaining_balance for loan in loans)
    total_monthly = sum(loan.monthly_deduction for loan in loans)
    
    context = {
        'loans': loans,
        'total_principal': total_principal,
        'total_outstanding': total_outstanding,
        'total_monthly': total_monthly,
    }
    return render(request, 'payroll/loan_management.html', context)

@login_required
@group_required('Staff')
def deduction_management(request):
    """Manage other deductions"""
    # Get all deductions (not just active ones for the table)
    deductions = OtherDeduction.objects.select_related('employee').all()
    
    # Calculate statistics
    total_deductions = deductions.count()
    active_deductions = deductions.filter(is_active=True).count()
    total_amount = sum(d.amount for d in deductions.filter(is_active=True))
    
    # Get active loans for the summary section and count them as loan deductions
    loans = Loan.objects.select_related('employee').filter(is_active=True)
    loan_deductions = loans.count()
    
    context = {
        'deductions': deductions,
        'total_deductions': total_deductions,
        'active_deductions': active_deductions,
        'total_amount': total_amount,
        'loan_deductions': loan_deductions,
        'loans': loans,
    }
    return render(request, 'payroll/deduction_management.html', context)

@login_required
def my_deposit_status(request):
    """Employee view of their salary deposit status"""
    try:
        employee = request.user.employee

        payslips = Payslip.objects.filter(employee=employee).select_related('payroll_run').order_by('-payroll_run__created_at')[:12]  # Last 12 payslips
        return render(request, 'payroll/my_deposit_status.html', {
            'payslips': payslips,
            'employee': employee
        })
    except Employee.DoesNotExist:
        return render(request, 'payroll/my_deposit_status.html', {
            'payslips': [],
            'employee': None,
            'error': 'No employee record found for your account. Please contact HR.'
        })

@login_required
def download_payslip_pdf(request, slip_id):
    """Download PDF payslip for employee"""
    try:
        emp = request.user.employee
        slip = get_object_or_404(Payslip, pk=slip_id, employee=emp)
    except Employee.DoesNotExist:
        messages.error(request, "No employee record found.")
        return redirect('my_payslips')
    
    # Generate PDF if not exists
    if not slip.pdf_file:
        pdf_buffer = generate_payslip_pdf(slip)
        slip.pdf_file.save(
            f'payslip_{slip.employee.employee_no}_{slip.payroll_run.id}.pdf',
            ContentFile(pdf_buffer.read())
        )
        slip.save()
    
    # Return PDF
    response = HttpResponse(slip.pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{slip.employee.employee_no}.pdf"'
    return response

@login_required
@group_required('Staff')
def generate_all_payslip_pdfs(request, run_id):
    """Generate PDFs for all payslips in a run"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    generated = 0
    
    for payslip in run.payslips.all():
        if not payslip.pdf_file:
            try:
                pdf_buffer = generate_payslip_pdf(payslip)
                payslip.pdf_file.save(
                    f'payslip_{payslip.employee.employee_no}_{run.id}.pdf',
                    ContentFile(pdf_buffer.read())
                )
                payslip.save()
                generated += 1
            except Exception as e:
                messages.warning(request, f"Error generating PDF for {payslip.employee}: {str(e)}")
    
    messages.success(request, f"Generated {generated} PDF payslips!")
    return redirect('payroll_run_payslips', run_id=run.id)

@login_required
@group_required('Staff')
def export_payroll_excel(request, run_id):
    """Export payroll run to Excel"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    excel_buffer = export_to_excel(run)
    
    response = HttpResponse(
        excel_buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="payroll_{run.id}.xlsx"'
    
    return response

@login_required
@group_required('Staff')
def edit_payroll_run(request, run_id):
    """Edit payroll run dates"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    # Only allow editing for DRAFT status
    if run.status != 'DRAFT':
        messages.error(request, "Cannot edit payroll run. Only DRAFT payroll runs can be edited.")
        return redirect('payroll_run_payslips', run_id=run.id)
    
    if request.method == 'POST':
        form = PayrollRunForm(request.POST, instance=run)
        if form.is_valid():
            form.save()
            messages.success(request, "Payroll run dates updated! Click 'Recalculate Payslips' to update calculations.")
            return redirect('payroll_run_payslips', run_id=run.id)
    else:
        form = PayrollRunForm(instance=run)
    
    return render(request, 'payroll/edit_payroll_run.html', {'form': form, 'run': run})

@login_required
@group_required('Staff')
def recalculate_payslips(request, run_id):
    """Recalculate all payslips for a payroll run"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    # Only allow recalculation for DRAFT status
    if run.status != 'DRAFT':
        messages.error(request, "Cannot recalculate payslips. Only DRAFT payroll runs can be recalculated.")
        return redirect('payroll_run_payslips', run_id=run.id)
    
    if request.method == 'POST':
        # Delete existing payslips
        deleted_count = run.payslips.count()
        run.payslips.all().delete()
        
        # Recalculate payslips for all active employees
        employees = Employee.objects.filter(active=True).select_related('salary_grade')
        payslips_created = 0
        
        for emp in employees:
            try:
                # Use PayrollCalculator with current dates
                calculator = PayrollCalculator(
                    employee=emp,
                    period_start=run.period_start,
                    period_end=run.period_end
                )
                
                payroll_data = calculator.compute_payslip()
                
                Payslip.objects.create(
                    payroll_run=run,
                    employee=emp,
                    **payroll_data
                )
                payslips_created += 1
            except Exception as e:
                messages.warning(request, f"Could not calculate payroll for {emp}: {str(e)}")
        
        messages.success(request, f"Payslips recalculated! Deleted {deleted_count} old payslips, created {payslips_created} new payslips.")
        return redirect('payroll_run_payslips', run_id=run.id)
    
    return render(request, 'payroll/confirm_recalculate.html', {'run': run})

@login_required
@group_required('Staff')
def update_payroll_status(request, run_id):
    """Update payroll run workflow status"""
    from django.utils import timezone
    
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status in ['REVIEW', 'APPROVED', 'PAID', 'CANCELLED']:
            run.status = new_status
            
            if new_status == 'REVIEW':
                run.reviewed_by = request.user
                run.reviewed_at = timezone.now()
            elif new_status == 'APPROVED':
                run.approved_by = request.user
                run.approved_at = timezone.now()
            elif new_status == 'PAID':
                run.paid_date = timezone.now()
                # Update loan balances
                for payslip in run.payslips.all():
                    update_loan_balances(payslip)
            
            run.save()
            messages.success(request, f"Payroll run status updated to {new_status}")
        else:
            messages.error(request, "Invalid status")
    
    return redirect('payroll_run_payslips', run_id=run.id)
