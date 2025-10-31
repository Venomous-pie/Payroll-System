

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
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('decided_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('decided_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AttendanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('time_out', models.TimeField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('employee', 'date')},
            },
        ),
    ]
