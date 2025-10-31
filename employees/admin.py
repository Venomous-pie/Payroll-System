from django.contrib import admin
from .models import Employee, SalaryGrade

@admin.register(SalaryGrade)
class SalaryGradeAdmin(admin.ModelAdmin):
    list_display = ("code", "step", "base_pay")
    list_filter = ("code",)
    search_fields = ("code",)
    ordering = ("code", "step")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_no", "last_name", "first_name", "department", "position", "salary_grade", "bank_name", "active", "date_hired")
    list_filter = ("department", "position", "active", "salary_grade", "bank_name")
    search_fields = ("employee_no", "last_name", "first_name", "user__username", "user__email")
    readonly_fields = ("user",)
    fieldsets = (
        ("Basic Information", {
            "fields": ("user", "employee_no", "first_name", "last_name")
        }),
        ("Employment Details", {
            "fields": ("department", "position", "salary_grade", "date_hired", "active")
        }),
        ("Bank Information", {
            "fields": ("bank_name", "bank_account")
        }),
    )
    ordering = ("employee_no",)
