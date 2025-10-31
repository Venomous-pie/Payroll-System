

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_employee_bank_account_employee_bank_name'),
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payslip',
            name='bank_file_generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payslip',
            name='bank_file_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payslip',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='payslip',
            name='deposit_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payslip',
            name='loan_deductions',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='payslip',
            name='other_deductions',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='payslip',
            name='overtime_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='payslip',
            name='salary_deposited',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.CharField(choices=[('SALARY', 'Salary Loan'), ('EMERGENCY', 'Emergency Loan'), ('HOUSING', 'Housing Loan'), ('OTHER', 'Other')], max_length=20)),
                ('principal_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('monthly_deduction', models.DecimalField(decimal_places=2, max_digits=12)),
                ('remaining_balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('start_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
        migrations.CreateModel(
            name='OtherDeduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_recurring', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
    ]
