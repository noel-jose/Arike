# Generated by Django 4.0.3 on 2022-03-07 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_customuser_district_alter_customuser_facility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.district'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.facility'),
        ),
    ]
