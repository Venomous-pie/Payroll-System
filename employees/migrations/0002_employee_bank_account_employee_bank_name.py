

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='bank_account',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='employee',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
