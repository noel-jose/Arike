# Generated by Django 4.0.3 on 2022-03-09 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_alter_familydetail_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.patient'),
        ),
    ]
