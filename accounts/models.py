from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=10)
    ip = models.CharField(max_length=64, blank=True)
    status_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} {self.user} {self.method} {self.path} {self.status_code}"
