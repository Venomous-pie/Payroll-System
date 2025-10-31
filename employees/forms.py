from django import forms
from django.contrib.auth import get_user_model
from .models import Employee, SalaryGrade

User = get_user_model()

class SalaryGradeForm(forms.ModelForm):
    class Meta:
        model = SalaryGrade
        fields = ['code', 'step', 'base_pay']

class EmployeeForm(forms.ModelForm):
    # User account fields
    username = forms.CharField(max_length=150, required=True, help_text="Username for system login")
    email = forms.EmailField(required=True, help_text="Email address for notifications")
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text="Initial password for the account")
    
    class Meta:
        model = Employee
        fields = ['employee_no', 'first_name', 'last_name', 'department', 'position', 'salary_grade', 'date_hired', 'bank_name', 'bank_account', 'active']
        widgets = {
            'date_hired': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_no': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_grade': forms.Select(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide user fields when updating (only show when creating)
        if self.instance and self.instance.pk:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['username'].required = False
            self.fields['email'].required = False
            self.fields['password'].required = False
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Only validate username on create
        if not self.instance.pk and username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Only validate email on create
        if not self.instance.pk and email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        return email
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        
        # Create user account if this is a new employee
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            employee.user = user
        
        if commit:
            employee.save()
        return employee
