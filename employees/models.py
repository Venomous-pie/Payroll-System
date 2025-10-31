from django.db import models
from django.conf import settings

class SalaryGrade(models.Model):
    code = models.CharField(max_length=20, unique=True)
    step = models.PositiveIntegerField(default=1)
    base_pay = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.code}-Step{self.step}"

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')
    employee_no = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary_grade = models.ForeignKey(SalaryGrade, on_delete=models.PROTECT)
    date_hired = models.DateField(null=True, blank=True)
    

    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_no} - {self.last_name}, {self.first_name}"
