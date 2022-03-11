# Generated by Django 4.0.3 on 2022-03-10 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_diseasehistory_created_at_diseasehistory_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitdetails',
            name='note',
        ),
        migrations.AddField(
            model_name='visitschedule',
            name='cancelled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='visitschedule',
            name='nurse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitschedule',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.patient'),
        ),
    ]