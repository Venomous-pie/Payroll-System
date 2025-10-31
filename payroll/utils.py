from decimal import Decimal
import csv
import io
from datetime import datetime
from django.http import HttpResponse


SSS_RATE = Decimal('0.045')  # placeholder employee share
PHILHEALTH_RATE = Decimal('0.035')  # placeholder shared; use half for employee
PAGIBIG_RATE = Decimal('0.01')  # placeholder employee share capped elsewhere
TAX_RATE = Decimal('0.10')  # placeholder withholding


def compute_contributions(gross: Decimal) -> dict:
    """Compute government contributions and taxes"""
    sss = (gross * SSS_RATE).quantize(Decimal('0.01'))
    philhealth = (gross * (PHILHEALTH_RATE / 2)).quantize(Decimal('0.01'))
    pagibig = (gross * PAGIBIG_RATE).quantize(Decimal('0.01'))

    taxable = gross - sss - philhealth - pagibig
    tax = (taxable * TAX_RATE).quantize(Decimal('0.01')) if taxable > 0 else Decimal('0.00')
    
    return {
        'sss': sss,
        'philhealth': philhealth,
        'pagibig': pagibig,
        'tax': tax,
    }

def compute_employee_deductions(employee):
    """Compute loan and other deductions for an employee"""
    from .models import Loan, OtherDeduction
    

    loans = Loan.objects.filter(employee=employee, is_active=True)
    loan_deductions = sum(loan.monthly_deduction for loan in loans)
    

    other_deductions = OtherDeduction.objects.filter(employee=employee, is_active=True)
    other_deduction_total = sum(deduction.amount for deduction in other_deductions)
    
    return {
        'loan_deductions': Decimal(str(loan_deductions)).quantize(Decimal('0.01')),
        'other_deductions': Decimal(str(other_deduction_total)).quantize(Decimal('0.01')),
    }

def compute_full_payroll(employee, gross_pay, overtime_pay=0):
    """Complete payroll computation following the flowchart"""
    gross_total = Decimal(str(gross_pay)) + Decimal(str(overtime_pay))
    

    contributions = compute_contributions(gross_total)
    

    deductions = compute_employee_deductions(employee)
    

    total_deductions = (
        contributions['sss'] + 
        contributions['philhealth'] + 
        contributions['pagibig'] + 
        contributions['tax'] +
        deductions['loan_deductions'] +
        deductions['other_deductions']
    )
    
    net_pay = gross_total - total_deductions
    
    return {
        'gross_pay': gross_total.quantize(Decimal('0.01')),
        'overtime_pay': Decimal(str(overtime_pay)).quantize(Decimal('0.01')),
        'sss': contributions['sss'],
        'philhealth': contributions['philhealth'],
        'pagibig': contributions['pagibig'],
        'tax': contributions['tax'],
        'loan_deductions': deductions['loan_deductions'],
        'other_deductions': deductions['other_deductions'],
        'net_pay': net_pay.quantize(Decimal('0.01')),
    }

def generate_bank_file(payroll_run):
    """Generate bank file for salary transfer (Step 8 in flowchart)"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="bank_transfer_{payroll_run.id}_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    output = io.StringIO()
    writer = csv.writer(output)
    

    writer.writerow([
        'Employee_ID', 'Employee_Name', 'Account_Number', 
        'Amount', 'Reference', 'Date'
    ])
    

    for payslip in payroll_run.payslips.select_related('employee').all():
        writer.writerow([
            payslip.employee.employee_no,
            f"{payslip.employee.first_name} {payslip.employee.last_name}",
            payslip.employee.bank_account or 'N/A',
            str(payslip.net_pay),
            f"Payroll_{payroll_run.id}",
            payroll_run.period_end.strftime('%Y-%m-%d')
        ])
    
    response.write(output.getvalue())
    return response
