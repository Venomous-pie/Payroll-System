

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sss', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('philhealth', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('pagibig', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('net_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employees.employee')),
                ('payroll_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to='payroll.payrollrun')),
            ],
        ),
    ]
