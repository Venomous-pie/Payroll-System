from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Employee, SalaryGrade
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with 10 sample employees'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting employee seeding...'))

        # Sample data
        first_names = ['Juan', 'Maria', 'Jose', 'Ana', 'Pedro', 'Rosa', 'Carlos', 'Elena', 'Miguel', 'Sofia']
        last_names = ['Dela Cruz', 'Santos', 'Reyes', 'Garcia', 'Ramos', 'Torres', 'Flores', 'Mendoza', 'Castro', 'Bautista']
        departments = ['Accounting', 'HR', 'IT', 'Sales', 'Operations', 'Marketing']
        positions = ['Staff', 'Senior Staff', 'Supervisor', 'Manager', 'Specialist']
        banks = ['BDO', 'BPI', 'Metrobank', 'UnionBank', 'Security Bank']

        # Check if salary grades exist
        salary_grades = SalaryGrade.objects.all()
        if not salary_grades.exists():
            self.stdout.write(self.style.ERROR('No salary grades found! Creating default salary grades...'))
            # Create default salary grades
            default_grades = [
                {'code': 'SG1', 'step': 1, 'base_pay': 15000.00},
                {'code': 'SG2', 'step': 1, 'base_pay': 20000.00},
                {'code': 'SG3', 'step': 1, 'base_pay': 25000.00},
                {'code': 'SG4', 'step': 1, 'base_pay': 30000.00},
                {'code': 'SG5', 'step': 1, 'base_pay': 40000.00},
            ]
            for grade_data in default_grades:
                SalaryGrade.objects.create(**grade_data)
            salary_grades = SalaryGrade.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Created {salary_grades.count()} default salary grades'))

        # Create 10 employees
        created_count = 0
        skipped_count = 0

        for i in range(1, 11):
            employee_no = f'EMP{i:03d}'
            username = f'employee{i}'

            # Check if employee already exists
            if Employee.objects.filter(employee_no=employee_no).exists():
                self.stdout.write(self.style.WARNING(f'Employee {employee_no} already exists, skipping...'))
                skipped_count += 1
                continue

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User {username} already exists, skipping...'))
                skipped_count += 1
                continue

            # Create user account
            first_name = first_names[i-1]
            last_name = last_names[i-1]
            
            user = User.objects.create_user(
                username=username,
                password='password123',  # Default password
                first_name=first_name,
                last_name=last_name,
                email=f'{username}@company.com'
            )

            # Create employee record
            employee = Employee.objects.create(
                user=user,
                employee_no=employee_no,
                first_name=first_name,
                last_name=last_name,
                department=random.choice(departments),
                position=random.choice(positions),
                salary_grade=random.choice(salary_grades),
                date_hired=date.today() - timedelta(days=random.randint(30, 730)),  # Hired 1 month to 2 years ago
                bank_name=random.choice(banks),
                bank_account=f'{random.randint(1000000000, 9999999999)}',
                active=True
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created: {employee_no} - {last_name}, {first_name} '
                    f'({employee.department} - {employee.position})'
                )
            )
            created_count += 1

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created {created_count} employees'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped {skipped_count} existing employees'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write(self.style.NOTICE('Default credentials for all employees:'))
        self.stdout.write(self.style.NOTICE('  Username: employee1, employee2, ..., employee10'))
        self.stdout.write(self.style.NOTICE('  Password: password123'))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('⚠ Remember to change passwords in production!'))
