# Generated by Django 4.0.3 on 2022-03-11 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0017_remove_treatmentnotes_notes_treatmentnotes_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='schedule_alert_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
