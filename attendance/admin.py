from django.contrib import admin
from django.utils.html import format_html
from .models import AttendanceLog, LeaveRequest

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ("date", "employee", "employee_no", "time_in", "time_out", "work_hours", "remarks", "created_at")
    list_filter = ("date", "employee__department", "employee__active")
    search_fields = ("employee__employee_no", "employee__last_name", "employee__first_name")
    date_hierarchy = "date"
    ordering = ("-date", "employee__employee_no")
    
    def employee_no(self, obj):
        return obj.employee.employee_no
    employee_no.short_description = "Employee ID"
    
    def work_hours(self, obj):
        if obj.time_in and obj.time_out:
            from datetime import datetime, timedelta
            time_in = datetime.combine(obj.date, obj.time_in)
            time_out = datetime.combine(obj.date, obj.time_out)
            if time_out < time_in:  # Handle overnight shifts
                time_out += timedelta(days=1)
            duration = time_out - time_in
            hours = duration.total_seconds() / 3600
            return f"{hours:.2f} hrs"
        return "Incomplete"
    work_hours.short_description = "Work Hours"

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "employee_no", "leave_type", "start_date", "end_date", "days_count", "status_badge", "decided_by", "created_at")
    list_filter = ("status", "leave_type", "start_date", "employee__department")
    search_fields = ("employee__employee_no", "employee__last_name", "employee__first_name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "decided_at")
    
    fieldsets = (
        ("Leave Request Information", {
            "fields": ("employee", "leave_type", "start_date", "end_date", "reason")
        }),
        ("Status & Decision", {
            "fields": ("status", "decided_by", "decided_at", "created_at")
        }),
    )
    
    def employee_no(self, obj):
        return obj.employee.employee_no
    employee_no.short_description = "Employee ID"
    
    def days_count(self, obj):
        if obj.start_date and obj.end_date:
            delta = obj.end_date - obj.start_date
            return f"{delta.days + 1} days"
        return "N/A"
    days_count.short_description = "Duration"
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#ffc107',
            'APPROVED': '#28a745',
            'REJECTED': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
