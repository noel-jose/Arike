# Generated by Django 4.0.3 on 2022-03-07 03:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(blank=True, max_length=150)),
                ('role', models.CharField(choices=[('Primary Nurse', 'Primary Nurse'), ('Secondary Nurse', 'Secondary Nurse'), ('District Admin', 'District Admin')], max_length=20)),
                ('phone', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')])),
                ('is_verified', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('icds_code', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lsgbody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('kind', models.CharField(choices=[('Grama Panchayath', 'Grama Panchayath'), ('Block Panchayath', 'Block Panchayath'), ('District Panchayath', 'District Panchayath'), ('Nagar Panchayath', 'Nagar Panchayath'), ('Municipality', 'Municipality'), ('Corporation', 'Corporation'), ('Others', 'Others')], max_length=20)),
                ('lsg_body_code', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.district')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField(default='')),
                ('landmark', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Non-binary', 'Non-binary')], max_length=20)),
                ('emergency_phone_number', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')])),
                ('expired_time', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('nurse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('care_type', models.CharField(choices=[('General care', 'General care'), ('Gastro-intestinal care', 'Gastro-intestinal care'), ('Wound care', 'Wound care')], max_length=150)),
                ('care_sub_type', models.CharField(choices=[('Perennial care', 'Perennial care'), ('Urostomy care', 'Urostomy care'), ('Ryles tube care', 'Ryles tube care')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.patient')),
            ],
        ),
        migrations.CreateModel(
            name='VisitSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('duration', models.CharField(max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('number', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('lsg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.lsgbody')),
            ],
        ),
        migrations.CreateModel(
            name='VisitDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pallative_phase', models.CharField(max_length=100)),
                ('blood_pressure', models.IntegerField()),
                ('pulse', models.IntegerField()),
                ('General_Random_Blood_Sugar', models.CharField(max_length=6)),
                ('Personal_hygiene', models.CharField(max_length=100)),
                ('Mouth_hygiene', models.CharField(max_length=100)),
                ('Public_hygiene', models.CharField(max_length=100)),
                ('systematic_examination', models.TextField()),
                ('patient_at_peace', models.BooleanField(default=True)),
                ('pain', models.BooleanField(default=True)),
                ('symptoms', models.TextField()),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('visit_schedule', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.visitschedule')),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.treatment')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.visitdetails')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.ward'),
        ),
        migrations.CreateModel(
            name='FamilyDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')])),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('relation', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Sibling', 'Sibling'), ('Relative', 'Relative')], max_length=20)),
                ('address', models.TextField(default='')),
                ('education', models.CharField(max_length=35)),
                ('occupation', models.CharField(max_length=35)),
                ('remarks', models.TextField()),
                ('is_primary', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=35)),
                ('address', models.TextField(default='')),
                ('pincode', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.ward')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.state'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.district'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apps.facility'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]