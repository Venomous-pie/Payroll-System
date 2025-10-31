from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import UserProfile, AuditLog


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_groups', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    def user_groups(self, obj):
        groups = obj.groups.all()
        if groups:
            group_names = [g.name for g in groups]
            colors = {'Admin': '#dc3545', 'Staff': '#28a745', 'Employee': '#007bff'}
            badges = []
            for group in group_names:
                color = colors.get(group, '#6c757d')
                badges.append(f'<span style="background: {color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; margin-right: 2px;">{group}</span>')
            return format_html(''.join(badges))
        return format_html('<span style="color: #999; font-style: italic;">No groups</span>')
    user_groups.short_description = 'Groups'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_email", "employee_id", "department", "position", "user_groups")
    list_filter = ("department", "position", "user__groups")
    search_fields = ("user__username", "user__email", "employee_id", "department", "position")
    ordering = ("user__username",)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"
    
    def user_groups(self, obj):
        groups = obj.user.groups.all()
        if groups:
            return ", ".join([g.name for g in groups])
        return "No groups"
    user_groups.short_description = "User Groups"

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "method_badge", "path", "status_badge", "ip")
    list_filter = ("method", "status_code", "created_at")
    search_fields = ("path", "ip", "user__username")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "user", "method", "path", "status_code", "ip")
    
    def method_badge(self, obj):
        colors = {
            'GET': '#17a2b8',
            'POST': '#28a745', 
            'PUT': '#ffc107',
            'DELETE': '#dc3545',
            'PATCH': '#6f42c1'
        }
        color = colors.get(obj.method, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">{}</span>',
            color, obj.method
        )
    method_badge.short_description = "Method"
    
    def status_badge(self, obj):
        if 200 <= obj.status_code < 300:
            color = '#28a745'  # Success - green
        elif 300 <= obj.status_code < 400:
            color = '#17a2b8'  # Redirect - blue
        elif 400 <= obj.status_code < 500:
            color = '#ffc107'  # Client error - yellow
        else:
            color = '#dc3545'  # Server error - red
            
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">{}</span>',
            color, obj.status_code
        )
    status_badge.short_description = "Status"
    


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count', 'permissions_count')
    search_fields = ('name',)
    
    def member_count(self, obj):
        count = obj.user_set.count()
        return f"{count} member{'s' if count != 1 else ''}"
    member_count.short_description = "Members"
    
    def permissions_count(self, obj):
        count = obj.permissions.count()
        return f"{count} permission{'s' if count != 1 else ''}"
    permissions_count.short_description = "Permissions"


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
