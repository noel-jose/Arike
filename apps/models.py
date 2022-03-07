from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


phone_number_regex = RegexValidator(
    regex=r"^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)


# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=35)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


LOCAL_BODY_CHOICES = (
    # Panchayath levels
    ("Grama Panchayath", "Grama Panchayath"),
    ("Block Panchayath", "Block Panchayath"),
    ("District Panchayath", "District Panchayath"),
    ("Nagar Panchayath", "Nagar Panchayath"),
    # Municipality levels
    ("Municipality", "Municipality"),
    # Corporation levels
    ("Corporation", "Corporation"),
    # Unknown
    ("Others", "Others"),
)


class Lsgbody(models.Model):
    name = models.CharField(max_length=35)
    kind = models.CharField(max_length=20, choices=LOCAL_BODY_CHOICES)
    lsg_body_code = models.CharField(max_length=20, unique=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    lsg = models.ForeignKey(Lsgbody, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


FACILITY_KIND = (("PHC", "PHC"), ("CHC", "CHC"))


class Facility(models.Model):
    kind = models.CharField(max_length=10, choices=FACILITY_KIND)
    name = models.CharField(max_length=35)
    address = models.TextField(default="")
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=14, validators=[phone_number_regex])
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


USER_ROLES = (
    ("Primary Nurse", "Primary Nurse"),
    ("Secondary Nurse", "Secondary Nurse"),
    ("District Admin", "District Admin"),
)


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=USER_ROLES, max_length=20, blank=False)
    phone = models.CharField(max_length=14, validators=[phone_number_regex])
    is_verified = models.BooleanField(default=True)
    district = models.ForeignKey(
        District, on_delete=models.PROTECT, blank=True, null=True
    )
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Non-binary", "Non-binary")]


class Patient(models.Model):
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    address = models.TextField(default="")
    landmark = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, validators=[phone_number_regex])
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    emergency_phone_number = models.CharField(
        max_length=14, validators=[phone_number_regex]
    )
    expired_time = models.DateTimeField(blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    nurse = models.ForeignKey(CustomUser, blank=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


RELATION = (
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Son", "Son"),
    ("Daughter", "Daughter"),
    ("Sibling", "Sibling"),
    ("Relative", "Relative"),
)


class FamilyDetail(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=14, validators=[phone_number_regex])
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True)
    relation = models.CharField(max_length=20, choices=RELATION)
    address = models.TextField(default="")
    education = models.CharField(max_length=35)
    occupation = models.CharField(max_length=35)
    remarks = models.TextField()
    is_primary = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class Disease(models.Model):
    name = models.CharField(max_length=35)
    icds_code = models.CharField(max_length=35)


class VisitSchedule(models.Model):
    date_time = models.DateTimeField()
    duration = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class VisitDetails(models.Model):
    pallative_phase = models.CharField(max_length=100)
    blood_pressure = models.IntegerField()
    pulse = models.IntegerField()
    General_Random_Blood_Sugar = models.CharField(max_length=6)
    Personal_hygiene = models.CharField(max_length=100)
    Mouth_hygiene = models.CharField(max_length=100)
    Public_hygiene = models.CharField(max_length=100)
    systematic_examination = models.TextField()
    patient_at_peace = models.BooleanField(default=True)
    pain = models.BooleanField(default=True)
    symptoms = models.TextField()
    note = models.TextField()
    visit_schedule = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


CARE_TYPE = (
    ("General care", "General care"),
    ("Gastro-intestinal care", "Gastro-intestinal care"),
    ("Wound care", "Wound care"),
)

CARE_SUB_TYPE = (
    ("Perennial care", "Perennial care"),
    ("Urostomy care", "Urostomy care"),
    ("Ryles tube care", "Ryles tube care"),
)


class Treatment(models.Model):
    description = models.TextField()
    care_type = models.CharField(choices=CARE_TYPE, max_length=150)
    care_sub_type = models.CharField(choices=CARE_SUB_TYPE, max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class TreatmentNotes(models.Model):
    notes = models.TextField()
    description = models.TextField()
    visit = models.ForeignKey(VisitDetails, on_delete=models.PROTECT)
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
