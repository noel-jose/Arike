# Generated by Django 4.0.3 on 2022-03-10 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_diseasehistory_delete_disease'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseasehistory',
            name='description',
            field=models.TextField(null=True),
        ),
    ]