# Generated by Django 4.0.3 on 2022-03-09 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_patient_nurse'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='facility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.facility'),
        ),
        migrations.AlterField(
            model_name='familydetail',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.patient'),
        ),
    ]
