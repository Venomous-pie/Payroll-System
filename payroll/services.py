"""
Payroll calculation services
Handles automated computation of salaries, deductions, and taxes
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum, Q
from contributions.models import SSSContributionTable, PhilHealthContributionTable, PagibigContributionTable, TaxTable
from attendance.models import AttendanceLog
from .models import Loan, OtherDeduction


class PayrollCalculator:
    """Service class for payroll calculations"""
    
    # Standard work hours per day
    STANDARD_HOURS_PER_DAY = Decimal('8.00')
    WORKING_DAYS_PER_MONTH = Decimal('22')  # Average
    
    def __init__(self, employee, period_start, period_end):
        self.employee = employee
        self.period_start = period_start
        self.period_end = period_end
        self.base_salary = employee.salary_grade.base_pay
        self.daily_rate = self.base_salary / self.WORKING_DAYS_PER_MONTH
        self.hourly_rate = self.daily_rate / self.STANDARD_HOURS_PER_DAY
    
    def calculate_gross_pay(self):
        """Calculate gross pay based on attendance"""
        # Get attendance records for the period
        attendance_records = AttendanceLog.objects.filter(
            employee=self.employee,
            date__gte=self.period_start,
            date__lte=self.period_end
        )
        
        total_days_worked = attendance_records.count()
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Employee: {self.employee.employee_no}")
        logger.info(f"Period: {self.period_start} to {self.period_end}")
        logger.info(f"Base Salary: {self.base_salary}")
        logger.info(f"Daily Rate: {self.daily_rate}")
        logger.info(f"Attendance records found: {total_days_worked}")
        
        # If no attendance records, pro-rate based on period length
        if total_days_worked == 0:
            days_in_period = (self.period_end - self.period_start).days + 1
            logger.info(f"Days in period: {days_in_period}")
            
            # Calculate how many working days in the period (assume 5-day work week)
            # For simplicity, we'll assume all days are working days unless you want to exclude weekends
            working_days = Decimal(str(days_in_period))
            
            # Pro-rate the salary based on working days
            gross_pay = self.daily_rate * working_days
            logger.info(f"Calculated gross pay (no attendance): {self.daily_rate} x {working_days} = {gross_pay}")
        else:
            # Calculate based on actual attendance
            gross_pay = self.daily_rate * Decimal(str(total_days_worked))
            logger.info(f"Calculated gross pay (with attendance): {self.daily_rate} x {total_days_worked} = {gross_pay}")
        
        return gross_pay.quantize(Decimal('0.01'))
    
    def calculate_overtime_pay(self):
        """Calculate overtime pay based on attendance records"""
        # This is a simplified version
        # In real implementation, you'd track actual overtime hours
        attendance_records = AttendanceLog.objects.filter(
            employee=self.employee,
            date__gte=self.period_start,
            date__lte=self.period_end
        )
        
        total_overtime_hours = Decimal('0.00')
        
        for record in attendance_records:
            if record.time_in and record.time_out:
                # Calculate hours worked
                time_in = datetime.combine(record.date, record.time_in)
                time_out = datetime.combine(record.date, record.time_out)
                
                # Handle overnight shift
                if time_out < time_in:
                    time_out += timedelta(days=1)
                
                hours_worked = (time_out - time_in).seconds / 3600
                hours_worked_decimal = Decimal(str(hours_worked))
                
                # OT is any hour beyond 8 hours
                if hours_worked_decimal > self.STANDARD_HOURS_PER_DAY:
                    overtime = hours_worked_decimal - self.STANDARD_HOURS_PER_DAY
                    total_overtime_hours += overtime
        
        # OT rate is 1.25x for regular OT
        overtime_pay = total_overtime_hours * self.hourly_rate * Decimal('1.25')
        
        return overtime_pay.quantize(Decimal('0.01'))
    
    def calculate_government_contributions(self, gross_pay):
        """Calculate SSS, PhilHealth, and Pag-IBIG contributions"""
        sss = SSSContributionTable.get_contribution(gross_pay)
        philhealth = PhilHealthContributionTable.get_contribution(gross_pay)
        pagibig = PagibigContributionTable.get_contribution(gross_pay)
        
        return {
            'sss': sss['employee'],
            'philhealth': philhealth['employee'],
            'pagibig': pagibig['employee'],
            'total': sss['employee'] + philhealth['employee'] + pagibig['employee']
        }
    
    def calculate_loan_deductions(self):
        """Calculate total loan deductions for the period"""
        active_loans = Loan.objects.filter(
            employee=self.employee,
            is_active=True,
            remaining_balance__gt=0
        )
        
        total_deduction = Decimal('0.00')
        
        for loan in active_loans:
            # Deduct monthly payment, but not more than remaining balance
            deduction = min(loan.monthly_deduction, loan.remaining_balance)
            total_deduction += deduction
        
        return total_deduction.quantize(Decimal('0.01'))
    
    def calculate_other_deductions(self):
        """Calculate other deductions (uniform, tools, etc.)"""
        deductions = OtherDeduction.objects.filter(
            employee=self.employee,
            is_active=True
        )
        
        total = Decimal('0.00')
        
        for deduction in deductions:
            if deduction.is_recurring:
                # Recurring deductions are applied every payroll
                total += deduction.amount
            else:
                # One-time deductions
                total += deduction.amount
                # Mark as inactive after deduction
                deduction.is_active = False
                deduction.save()
        
        return total.quantize(Decimal('0.01'))
    
    def calculate_withholding_tax(self, gross_pay, total_deductions):
        """Calculate withholding tax"""
        # Compute annual taxable income
        # Simplified: multiply monthly by 12
        monthly_taxable = gross_pay - total_deductions
        annual_taxable = monthly_taxable * 12
        
        # Get annual tax
        annual_tax = TaxTable.get_withholding_tax(annual_taxable)
        
        # Return monthly tax
        monthly_tax = annual_tax / 12
        
        return monthly_tax.quantize(Decimal('0.01'))
    
    def compute_payslip(self):
        """Complete payroll computation"""
        # Calculate earnings
        gross_pay = self.calculate_gross_pay()
        overtime_pay = self.calculate_overtime_pay()
        total_earnings = gross_pay + overtime_pay
        
        # Calculate deductions
        gov_contributions = self.calculate_government_contributions(total_earnings)
        loan_deductions = self.calculate_loan_deductions()
        other_deductions = self.calculate_other_deductions()
        
        # Calculate tax (after mandatory contributions)
        total_mandatory_deductions = gov_contributions['total']
        tax = self.calculate_withholding_tax(total_earnings, total_mandatory_deductions)
        
        # Calculate net pay
        total_deductions = (
            gov_contributions['sss'] +
            gov_contributions['philhealth'] +
            gov_contributions['pagibig'] +
            tax +
            loan_deductions +
            other_deductions
        )
        
        net_pay = total_earnings - total_deductions
        
        return {
            'gross_pay': gross_pay,
            'overtime_pay': overtime_pay,
            'sss': gov_contributions['sss'],
            'philhealth': gov_contributions['philhealth'],
            'pagibig': gov_contributions['pagibig'],
            'tax': tax,
            'loan_deductions': loan_deductions,
            'other_deductions': other_deductions,
            'net_pay': net_pay
        }


def update_loan_balances(payslip):
    """Update loan balances after payroll processing"""
    employee = payslip.employee
    amount_deducted = payslip.loan_deductions
    
    if amount_deducted <= 0:
        return
    
    active_loans = Loan.objects.filter(
        employee=employee,
        is_active=True,
        remaining_balance__gt=0
    ).order_by('start_date')
    
    remaining_to_deduct = amount_deducted
    
    for loan in active_loans:
        if remaining_to_deduct <= 0:
            break
        
        deduction = min(loan.monthly_deduction, loan.remaining_balance, remaining_to_deduct)
        loan.remaining_balance -= deduction
        
        if loan.remaining_balance <= 0:
            loan.is_active = False
        
        loan.save()
        remaining_to_deduct -= deduction
