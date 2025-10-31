from django.db import models
from django.conf import settings
from employees.models import Employee

class PayrollRun(models.Model):
    """Payroll run with workflow states"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payroll_runs_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='payroll_runs_reviewed')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='payroll_runs_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    paid_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PayrollRun {self.period_start} to {self.period_end} ({self.status})"

class Loan(models.Model):
    """Employee loan management"""
    LOAN_TYPES = (
        ('SALARY', 'Salary Loan'),
        ('EMERGENCY', 'Emergency Loan'),
        ('HOUSING', 'Housing Loan'),
        ('OTHER', 'Other'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_deduction = models.DecimalField(max_digits=12, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee} - {self.loan_type} Loan"

class OtherDeduction(models.Model):
    """Other deductions like uniform, tools, etc."""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee} - {self.description}"

class Payslip(models.Model):
    """Individual payslip with detailed breakdown"""
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    
    # Earnings
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    holiday_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    night_differential = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Government deductions
    sss = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    philhealth = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagibig = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Other deductions
    loan_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Net pay
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Attendance details
    days_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tardiness_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    absences = models.IntegerField(default=0)
    
    # Bank transfer tracking
    bank_file_generated = models.BooleanField(default=False)
    bank_file_sent = models.BooleanField(default=False)
    salary_deposited = models.BooleanField(default=False)
    deposit_date = models.DateTimeField(null=True, blank=True)
    
    # PDF payslip
    pdf_file = models.FileField(upload_to='payslips/', null=True, blank=True)
    pdf_sent = models.BooleanField(default=False)
    pdf_sent_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['payroll_run', 'employee']

    def __str__(self):
        return f"Payslip {self.employee} {self.payroll_run}"
    
    @property
    def total_earnings(self):
        return self.gross_pay + self.overtime_pay + self.holiday_pay + self.night_differential + self.allowances
    
    @property
    def total_deductions(self):
        return self.sss + self.philhealth + self.pagibig + self.tax + self.loan_deductions + self.other_deductions
