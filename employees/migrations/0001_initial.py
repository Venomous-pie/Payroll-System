

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('step', models.PositiveIntegerField(default=1)),
                ('base_pay', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_no', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('date_hired', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('salary_grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employees.salarygrade')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
