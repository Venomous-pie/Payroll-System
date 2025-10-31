from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db import models
from employees.models import Employee, SalaryGrade
from attendance.models import AttendanceLog, LeaveRequest
from payroll.models import PayrollRun, Payslip, Loan, OtherDeduction
from contributions.models import SSSContributionTable, PhilHealthContributionTable, PagibigContributionTable, TaxTable
from datetime import date, datetime, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seeds the complete system with realistic data for 1+ year of operations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--months',
            type=int,
            default=14,
            help='Number of months of historical data to generate (default: 14)'
        )

    def handle(self, *args, **options):
        months = options['months']
        self.stdout.write(self.style.WARNING(f'Starting complete system seeding ({months} months of data)...'))
        self.stdout.write('')

        # Step 1: Create contribution tables
        self.create_contribution_tables()

        # Step 2: Create salary grades
        self.create_salary_grades()

        # Step 3: Create groups
        self.create_groups()

        # Step 4: Create users (admin, staff, employees)
        self.create_users()

        # Step 5: Create employees
        self.create_employees()

        # Step 6: Create historical attendance (past months)
        self.create_attendance_records(months)

        # Step 7: Create leave requests
        self.create_leave_requests()

        # Step 8: Create loans
        self.create_loans()

        # Step 9: Create other deductions
        self.create_other_deductions()

        # Step 10: Create historical payroll runs
        self.create_payroll_runs(months)

        # Final summary
        self.print_summary()

    def create_contribution_tables(self):
        self.stdout.write(self.style.NOTICE('📊 Creating contribution tables...'))
        
        # SSS Contribution Table (sample brackets)
        sss_brackets = [
            (0, 4249.99, 180, 540, 10, 730),
            (4250, 4749.99, 202.50, 607.50, 10, 820),
            (4750, 5249.99, 225, 675, 10, 910),
            (5250, 5749.99, 247.50, 742.50, 10, 1000),
            (10000, 10749.99, 450, 1350, 10, 1810),
            (15000, 15749.99, 675, 2025, 10, 2710),
            (20000, 20749.99, 900, 2700, 10, 3610),
            (25000, 26249.99, 1125, 3375, 10, 4510),
            (30000, 34999.99, 1350, 4050, 10, 5410),
            (35000, 39999.99, 1575, 4725, 10, 6310),
            (40000, 50000, 1800, 5400, 10, 7210),
        ]
        
        for min_sal, max_sal, ee, er, ec, total in sss_brackets:
            SSSContributionTable.objects.get_or_create(
                min_salary=Decimal(str(min_sal)),
                max_salary=Decimal(str(max_sal)),
                defaults={
                    'employee_share': Decimal(str(ee)),
                    'employer_share': Decimal(str(er)),
                    'ec_share': Decimal(str(ec)),
                    'total': Decimal(str(total)),
                    'effective_date': date(2024, 1, 1),
                    'is_active': True
                }
            )
        
        # PhilHealth
        PhilHealthContributionTable.objects.get_or_create(
            min_salary=Decimal('0'),
            defaults={
                'premium_rate': Decimal('0.05'),
                'max_contribution': Decimal('5000.00'),
                'effective_date': date(2024, 1, 1),
                'is_active': True
            }
        )
        
        # Pag-IBIG
        PagibigContributionTable.objects.get_or_create(
            min_salary=Decimal('0'),
            defaults={
                'employee_rate': Decimal('0.02'),
                'employer_rate': Decimal('0.02'),
                'max_employee_contribution': Decimal('100.00'),
                'max_employer_contribution': Decimal('100.00'),
                'effective_date': date(2024, 1, 1),
                'is_active': True
            }
        )
        
        # Tax Table (BIR 2024)
        tax_brackets = [
            (0, 250000, 0, 0),
            (250000, 400000, 0, 0.15),
            (400000, 800000, 22500, 0.20),
            (800000, 2000000, 102500, 0.25),
            (2000000, 8000000, 402500, 0.30),
            (8000000, 999999999, 2202500, 0.35),
        ]
        
        for min_comp, max_comp, base, rate in tax_brackets:
            TaxTable.objects.get_or_create(
                min_compensation=Decimal(str(min_comp)),
                max_compensation=Decimal(str(max_comp)),
                defaults={
                    'base_tax': Decimal(str(base)),
                    'tax_rate': Decimal(str(rate)),
                    'effective_date': date(2024, 1, 1),
                    'is_active': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created contribution tables'))

    def create_salary_grades(self):
        self.stdout.write(self.style.NOTICE('💰 Creating salary grades...'))
        
        grades = [
            ('SG1', 1, 15000),
            ('SG2', 1, 20000),
            ('SG3', 1, 25000),
            ('SG4', 1, 30000),
            ('SG5', 1, 35000),
            ('SG6', 1, 40000),
            ('SG7', 1, 50000),
            ('SG8', 1, 60000),
        ]
        
        for code, step, pay in grades:
            SalaryGrade.objects.get_or_create(
                code=code,
                step=step,
                defaults={'base_pay': Decimal(str(pay))}
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(grades)} salary grades'))

    def create_groups(self):
        self.stdout.write(self.style.NOTICE('👥 Creating user groups...'))
        
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='Staff')
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created user groups'))

    def create_users(self):
        self.stdout.write(self.style.NOTICE('🔐 Creating users...'))
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@company.com',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Created superuser: admin / admin123'))
        
        # Create staff user
        if not User.objects.filter(username='hr_staff').exists():
            staff_user = User.objects.create_user(
                username='hr_staff',
                password='staff123',
                email='hr@company.com',
                first_name='HR',
                last_name='Staff'
            )
            staff_group = Group.objects.get(name='Staff')
            staff_user.groups.add(staff_group)
            self.stdout.write(self.style.SUCCESS('  ✓ Created staff user: hr_staff / staff123'))

    def create_employees(self):
        self.stdout.write(self.style.NOTICE('👤 Creating employees...'))
        
        employees_data = [
            ('Juan', 'Dela Cruz', 'Accounting', 'Senior Accountant', 'SG5'),
            ('Maria', 'Santos', 'HR', 'HR Manager', 'SG6'),
            ('Jose', 'Reyes', 'IT', 'IT Specialist', 'SG5'),
            ('Ana', 'Garcia', 'Sales', 'Sales Manager', 'SG6'),
            ('Pedro', 'Ramos', 'Operations', 'Operations Supervisor', 'SG5'),
            ('Rosa', 'Torres', 'Marketing', 'Marketing Coordinator', 'SG4'),
            ('Carlos', 'Flores', 'Accounting', 'Staff Accountant', 'SG3'),
            ('Elena', 'Mendoza', 'IT', 'Junior Developer', 'SG3'),
            ('Miguel', 'Castro', 'Sales', 'Sales Representative', 'SG3'),
            ('Sofia', 'Bautista', 'HR', 'HR Assistant', 'SG2'),
            ('Ricardo', 'Villanueva', 'Operations', 'Warehouse Staff', 'SG2'),
            ('Carmen', 'Aquino', 'Accounting', 'Accounting Clerk', 'SG2'),
            ('Luis', 'Fernandez', 'IT', 'IT Support', 'SG3'),
            ('Isabella', 'Morales', 'Marketing', 'Marketing Assistant', 'SG2'),
            ('Gabriel', 'Navarro', 'Sales', 'Sales Associate', 'SG2'),
        ]
        
        banks = ['BDO', 'BPI', 'Metrobank', 'UnionBank', 'Security Bank', 'Landbank', 'PNB']
        created = 0
        
        for i, (first, last, dept, pos, sg_code) in enumerate(employees_data, 1):
            emp_no = f'EMP{i:03d}'
            username = f'employee{i}'
            
            if Employee.objects.filter(employee_no=emp_no).exists():
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password='password123',
                first_name=first,
                last_name=last,
                email=f'{username}@company.com'
            )
            
            # Create employee
            salary_grade = SalaryGrade.objects.get(code=sg_code, step=1)
            hire_date = date.today() - timedelta(days=random.randint(400, 800))  # 13-26 months ago
            
            Employee.objects.create(
                user=user,
                employee_no=emp_no,
                first_name=first,
                last_name=last,
                department=dept,
                position=pos,
                salary_grade=salary_grade,
                date_hired=hire_date,
                bank_name=random.choice(banks),
                bank_account=f'{random.randint(100000000000, 999999999999)}',
                active=True
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} employees'))

    def create_attendance_records(self, months):
        self.stdout.write(self.style.NOTICE(f'📅 Creating {months} months of attendance records...'))
        
        employees = Employee.objects.filter(active=True)
        total_records = 0
        
        # Generate attendance for past months
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)
        
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue
            
            for employee in employees:
                # 95% attendance rate (some absences)
                if random.random() < 0.95:
                    # Regular work hours with some variation
                    time_in_hour = random.choice([7, 8, 8, 8, 9])  # Mostly 8am
                    time_out_hour = random.choice([16, 17, 17, 17, 18])  # Mostly 5pm
                    
                    time_in = datetime.combine(current_date, datetime.min.time()).replace(
                        hour=time_in_hour, minute=random.randint(0, 59)
                    )
                    time_out = datetime.combine(current_date, datetime.min.time()).replace(
                        hour=time_out_hour, minute=random.randint(0, 59)
                    )
                    
                    # Occasional overtime (10% chance)
                    if random.random() < 0.1:
                        time_out = time_out.replace(hour=random.randint(19, 21))
                    
                    AttendanceLog.objects.get_or_create(
                        employee=employee,
                        date=current_date,
                        defaults={
                            'time_in': time_in.time(),
                            'time_out': time_out.time(),
                            'remarks': random.choice(['', '', '', 'On time', 'Overtime']) if random.random() < 0.2 else ''
                        }
                    )
                    total_records += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {total_records} attendance records'))

    def create_leave_requests(self):
        self.stdout.write(self.style.NOTICE('🏖️ Creating leave requests...'))
        
        employees = Employee.objects.filter(active=True)
        leave_types = ['Sick Leave', 'Vacation Leave', 'Emergency Leave', 'Personal Leave']
        statuses = ['APPROVED', 'APPROVED', 'APPROVED', 'PENDING', 'REJECTED']
        
        created = 0
        for employee in employees:
            # Each employee has 2-5 leave requests over the year
            num_leaves = random.randint(2, 5)
            for _ in range(num_leaves):
                leave_date = date.today() - timedelta(days=random.randint(30, 400))
                
                LeaveRequest.objects.create(
                    employee=employee,
                    leave_type=random.choice(leave_types),
                    start_date=leave_date,
                    end_date=leave_date + timedelta(days=random.randint(1, 3)),
                    reason=f'Personal matters',
                    status=random.choice(statuses)
                )
                created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} leave requests'))

    def create_loans(self):
        self.stdout.write(self.style.NOTICE('💳 Creating employee loans...'))
        
        employees = list(Employee.objects.filter(active=True))
        loan_types = ['Salary Loan', 'Emergency Loan', 'Calamity Loan']
        
        # 60% of employees have loans
        employees_with_loans = random.sample(employees, int(len(employees) * 0.6))
        
        created = 0
        for employee in employees_with_loans:
            principal = Decimal(random.choice([10000, 15000, 20000, 25000, 30000, 50000]))
            monthly = Decimal(random.choice([2000, 2500, 3000, 5000]))
            start_date = date.today() - timedelta(days=random.randint(60, 300))
            
            # Calculate remaining balance based on months elapsed
            months_elapsed = (date.today().year - start_date.year) * 12 + (date.today().month - start_date.month)
            paid_amount = monthly * min(months_elapsed, int(principal / monthly))
            remaining = max(Decimal('0'), principal - paid_amount)
            
            Loan.objects.create(
                employee=employee,
                loan_type=random.choice(loan_types),
                principal_amount=principal,
                remaining_balance=remaining,
                monthly_deduction=monthly,
                start_date=start_date,
                is_active=remaining > 0
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} loans'))

    def create_other_deductions(self):
        self.stdout.write(self.style.NOTICE('📝 Creating other deductions...'))
        
        employees = list(Employee.objects.filter(active=True))
        deduction_types = [
            ('Uniform', 500, False),
            ('ID Replacement', 200, False),
            ('Parking Fee', 500, True),
            ('Meal Deduction', 1000, True),
            ('Equipment Damage', 1500, False),
        ]
        
        # 40% of employees have deductions
        employees_with_deductions = random.sample(employees, int(len(employees) * 0.4))
        
        created = 0
        for employee in employees_with_deductions:
            desc, amount, recurring = random.choice(deduction_types)
            
            OtherDeduction.objects.create(
                employee=employee,
                description=desc,
                amount=Decimal(str(amount)),
                is_recurring=recurring,
                is_active=True
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} other deductions'))

    def create_payroll_runs(self, months):
        self.stdout.write(self.style.NOTICE(f'💰 Creating {months} months of payroll runs...'))
        
        # Get admin user for created_by
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        
        employees = Employee.objects.filter(active=True)
        
        # Generate bi-monthly payroll (1-15, 16-end of month)
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)
        
        current_month = start_date.replace(day=1)
        payroll_count = 0
        
        while current_month <= end_date:
            # First half of month (1-15)
            period_start = current_month
            period_end = current_month.replace(day=15)
            
            if period_end <= end_date:
                self.create_single_payroll_run(period_start, period_end, employees, admin_user)
                payroll_count += 1
            
            # Second half of month (16-end)
            period_start = current_month.replace(day=16)
            # Get last day of month
            if current_month.month == 12:
                next_month = current_month.replace(year=current_month.year + 1, month=1)
            else:
                next_month = current_month.replace(month=current_month.month + 1)
            period_end = next_month - timedelta(days=1)
            
            if period_end <= end_date:
                self.create_single_payroll_run(period_start, period_end, employees, admin_user)
                payroll_count += 1
            
            # Move to next month
            if current_month.month == 12:
                current_month = current_month.replace(year=current_month.year + 1, month=1)
            else:
                current_month = current_month.replace(month=current_month.month + 1)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {payroll_count} payroll runs'))

    def create_single_payroll_run(self, period_start, period_end, employees, admin_user):
        """Create a single payroll run with payslips"""
        
        # Determine status based on how old it is
        days_ago = (date.today() - period_end).days
        if days_ago > 30:
            status = 'PAID'
        elif days_ago > 15:
            status = 'APPROVED'
        elif days_ago > 7:
            status = 'REVIEW'
        else:
            status = 'DRAFT'
        
        # Create payroll run
        payroll_run = PayrollRun.objects.create(
            period_start=period_start,
            period_end=period_end,
            status=status,
            created_by=admin_user,
            created_at=datetime.combine(period_end + timedelta(days=1), datetime.min.time())
        )
        
        # Create payslips for each employee
        for employee in employees:
            # Calculate days worked
            attendance_count = AttendanceLog.objects.filter(
                employee=employee,
                date__gte=period_start,
                date__lte=period_end
            ).count()
            
            if attendance_count == 0:
                continue  # Skip if no attendance
            
            # Basic calculations
            daily_rate = employee.salary_grade.base_pay / 22  # Assuming 22 working days
            gross_pay = daily_rate * attendance_count
            
            # Calculate proration factor (for bi-monthly: 15 days is full, less is prorated)
            expected_days = 11  # Typical bi-monthly period has ~11 working days
            proration = min(Decimal(str(attendance_count)) / Decimal(str(expected_days)), Decimal('1.0'))
            
            # Simple deductions (would use actual calculation in production)
            sss = gross_pay * Decimal('0.045')  # Simplified
            philhealth = gross_pay * Decimal('0.025')
            pagibig = Decimal('100.00') * proration  # Prorate Pag-IBIG
            tax = gross_pay * Decimal('0.05') if gross_pay > 20000 else Decimal('0')
            
            # Loan deduction (prorate for bi-monthly: half of monthly)
            loan = Loan.objects.filter(employee=employee, is_active=True).first()
            loan_deduction = (loan.monthly_deduction / 2) * proration if loan else Decimal('0')
            
            # Other deductions (prorate for bi-monthly)
            other_ded_total = OtherDeduction.objects.filter(employee=employee, is_active=True).aggregate(
                total=models.Sum('amount')
            )['total'] or Decimal('0')
            other_ded = (other_ded_total / 2) * proration  # Half for bi-monthly
            
            net_pay = gross_pay - sss - philhealth - pagibig - tax - loan_deduction - other_ded
            
            Payslip.objects.create(
                payroll_run=payroll_run,
                employee=employee,
                gross_pay=gross_pay,
                sss=sss,
                philhealth=philhealth,
                pagibig=pagibig,
                tax=tax,
                loan_deductions=loan_deduction,
                other_deductions=other_ded,
                net_pay=net_pay,
                days_worked=attendance_count
            )

    def print_summary(self):
        from django.db import models
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('✓ COMPLETE SYSTEM SEEDING FINISHED!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        
        # Count everything
        self.stdout.write(self.style.NOTICE('📊 System Statistics:'))
        self.stdout.write(f'  👥 Employees: {Employee.objects.count()}')
        self.stdout.write(f'  💰 Salary Grades: {SalaryGrade.objects.count()}')
        self.stdout.write(f'  📅 Attendance Records: {AttendanceLog.objects.count()}')
        self.stdout.write(f'  🏖️ Leave Requests: {LeaveRequest.objects.count()}')
        self.stdout.write(f'  💳 Active Loans: {Loan.objects.filter(is_active=True).count()}')
        self.stdout.write(f'  📝 Other Deductions: {OtherDeduction.objects.count()}')
        self.stdout.write(f'  💰 Payroll Runs: {PayrollRun.objects.count()}')
        self.stdout.write(f'  📄 Payslips: {Payslip.objects.count()}')
        self.stdout.write('')
        
        # Payroll status breakdown
        self.stdout.write(self.style.NOTICE('📊 Payroll Status Breakdown:'))
        for status in ['DRAFT', 'REVIEW', 'APPROVED', 'PAID']:
            count = PayrollRun.objects.filter(status=status).count()
            self.stdout.write(f'  {status}: {count}')
        self.stdout.write('')
        
        self.stdout.write(self.style.NOTICE('🔐 Login Credentials:'))
        self.stdout.write('  Superuser:')
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: admin123')
        self.stdout.write('')
        self.stdout.write('  Staff/HR:')
        self.stdout.write('    Username: hr_staff')
        self.stdout.write('    Password: staff123')
        self.stdout.write('')
        self.stdout.write('  Employees:')
        self.stdout.write('    Username: employee1, employee2, ..., employee15')
        self.stdout.write('    Password: password123')
        self.stdout.write('')
        
        self.stdout.write(self.style.WARNING('⚠️ This is test data. Change passwords in production!'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Your payroll system is now fully populated!'))
        self.stdout.write(self.style.SUCCESS('   Visit http://127.0.0.1:8000/ to explore the system.'))
        self.stdout.write('')
