from django.contrib import admin
from django.utils.html import format_html
from .models import PayrollRun, Payslip, Loan, OtherDeduction

@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ("id", "pay_period", "employee_count", "total_gross", "total_net", "created_by", "created_at")
    list_filter = ("period_start", "period_end", "created_by")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    
    def pay_period(self, obj):
        return f"{obj.period_start.strftime('%b %d')} - {obj.period_end.strftime('%b %d, %Y')}"
    pay_period.short_description = "Pay Period"
    
    def employee_count(self, obj):
        return obj.payslips.count()
    employee_count.short_description = "Employees"
    
    def total_gross(self, obj):
        total = sum(p.gross_pay for p in obj.payslips.all())
        return f"₱{total:,.2f}"
    total_gross.short_description = "Total Gross"
    
    def total_net(self, obj):
        total = sum(p.net_pay for p in obj.payslips.all())
        return f"₱{total:,.2f}"
    total_net.short_description = "Total Net"

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ("employee", "employee_no", "payroll_period", "gross_pay", "total_deductions", "net_pay", "bank_status", "deposit_status")
    list_filter = ("payroll_run", "bank_file_generated", "salary_deposited", "employee__department")
    search_fields = ("employee__employee_no", "employee__last_name", "employee__first_name")
    date_hierarchy = "created_at"
    ordering = ("-payroll_run__created_at", "employee__employee_no")
    readonly_fields = ("created_at",)
    
    fieldsets = (
        ("Employee & Period", {
            "fields": ("employee", "payroll_run")
        }),
        ("Earnings", {
            "fields": ("gross_pay", "overtime_pay")
        }),
        ("Government Deductions", {
            "fields": ("sss", "philhealth", "pagibig", "tax")
        }),
        ("Other Deductions", {
            "fields": ("loan_deductions", "other_deductions")
        }),
        ("Final Amount", {
            "fields": ("net_pay",)
        }),
        ("Bank Transfer Status", {
            "fields": ("bank_file_generated", "bank_file_sent", "salary_deposited", "deposit_date", "created_at")
        }),
    )
    
    def employee_no(self, obj):
        return obj.employee.employee_no
    employee_no.short_description = "Employee ID"
    
    def payroll_period(self, obj):
        return f"{obj.payroll_run.period_start.strftime('%b %d')} - {obj.payroll_run.period_end.strftime('%b %d')}"
    payroll_period.short_description = "Period"
    
    def total_deductions(self, obj):
        total = obj.sss + obj.philhealth + obj.pagibig + obj.tax + obj.loan_deductions + obj.other_deductions
        return f"₱{total:,.2f}"
    total_deductions.short_description = "Total Deductions"
    
    def bank_status(self, obj):
        if obj.bank_file_generated:
            return format_html('<span style="color: #28a745;">✓ Generated</span>')
        return format_html('<span style="color: #dc3545;">✗ Pending</span>')
    bank_status.short_description = "Bank File"
    
    def deposit_status(self, obj):
        if obj.salary_deposited:
            return format_html('<span style="color: #28a745;">✓ Deposited</span>')
        elif obj.bank_file_sent:
            return format_html('<span style="color: #ffc107;">⏳ Processing</span>')
        return format_html('<span style="color: #dc3545;">✗ Pending</span>')
    deposit_status.short_description = "Deposit Status"

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("employee", "employee_no", "loan_type", "principal_amount", "monthly_deduction", "remaining_balance", "is_active", "start_date")
    list_filter = ("loan_type", "is_active", "start_date", "employee__department")
    search_fields = ("employee__employee_no", "employee__last_name", "employee__first_name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Employee Information", {
            "fields": ("employee",)
        }),
        ("Loan Details", {
            "fields": ("loan_type", "principal_amount", "monthly_deduction", "remaining_balance", "start_date")
        }),
        ("Status", {
            "fields": ("is_active", "created_at")
        }),
    )
    readonly_fields = ("created_at",)
    
    def employee_no(self, obj):
        return obj.employee.employee_no
    employee_no.short_description = "Employee ID"

@admin.register(OtherDeduction)
class OtherDeductionAdmin(admin.ModelAdmin):
    list_display = ("employee", "employee_no", "description", "amount", "is_recurring", "is_active", "created_at")
    list_filter = ("is_recurring", "is_active", "employee__department")
    search_fields = ("employee__employee_no", "employee__last_name", "employee__first_name", "description")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Employee Information", {
            "fields": ("employee",)
        }),
        ("Deduction Details", {
            "fields": ("description", "amount", "is_recurring")
        }),
        ("Status", {
            "fields": ("is_active", "created_at")
        }),
    )
    readonly_fields = ("created_at",)
    
    def employee_no(self, obj):
        return obj.employee.employee_no
    employee_no.short_description = "Employee ID"
