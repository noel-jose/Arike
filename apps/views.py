from operator import mod
from pyexpat import model
from django.shortcuts import render

from .models import CustomUser, Facility, Patient

# Create your views here.


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from django.forms import ChoiceField, ModelForm, TimeInput
from django import forms

from .models import FACILITY_KIND, GENDER_CHOICES


class CustomUserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "p-2 bg-gray-100 rounded-md outline-0", "size": 40}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "p-2 bg-gray-100 rounded-md outline-0", "size": 40}
        )


class UserLoginView(LoginView):
    form_class = CustomUserAuthenticationForm
    template_name = "login.html"


"""

    Creating views for Custom user

"""


class UsersListView(ListView):
    template_name = "User/customuser_list.html"
    context_object_name = "users"

    def get_queryset(self):
        users = CustomUser.objects.filter(deleted=False)
        return users


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "full_name",
            "username",
            "email",
            "password",
            "phone",
            "role",
            "district",
            "facility",
        ]
        exclude = [
            "is_staff",
            "is_active",
            "deleted",
            "last_login",
            "groups",
            "user_permissions",
            "is_superuser",
        ]
        # field_order = ["full_name", "email", "password", "phone"]


class UsersCreateView(CreateView):
    form_class = CustomUserForm
    template_name = "User/customuser_create.html"
    success_url = "/login"


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "User/customuser_update.html"
    success_url = "/dashboard"


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "User/customuser_detail.html"


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = "User/customuser_delete.html"
    success_url = "/dashboard"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


""" 

    Creating Views for Facilities 

"""


class FacilityListView(ListView):
    template_name = "Facility/list.html"
    context_object_name = "facilities"

    def get_queryset(self):
        facilities = Facility.objects.filter(deleted=False)
        return facilities


class FacilityForm(ModelForm):
    kind = forms.ChoiceField(choices=FACILITY_KIND, widget=forms.RadioSelect)

    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "pincode", "phone", "ward"]


class FacilityCreateView(CreateView):
    form_class = FacilityForm
    template_name = "Facility/create.html"
    success_url = "/list/facility"


class FacilityUpdateView(UpdateView):
    model = Facility
    form_class = FacilityForm
    template_name = "Facility/update.html"
    success_url = "/list/facility"


class FacilityDetailView(DetailView):
    model = Facility
    template_name = "Facility/detail.html"


class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = "Facility/delete.html"
    success_url = "/list/facility"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


"""

    Creating views for Patients

"""


class PatientListView(ListView):
    model = Patient
    template_name = "Patient/list.html"
    context_object_name = "patients"

    def get_queryset(self):
        if self.request.user.role == "District Admin":
            patients = Patient.objects.filter(deleted=False)
        else:
            patients = Patient.objects.filter(deleted=False, nurse=self.request.user)
        return patients


class PatientForm(ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Patient
        fields = [
            "full_name",
            "date_of_birth",
            "phone",
            "emergency_phone_number",
            "address",
            "landmark",
            "gender",
            "ward",
            "expired_time",
        ]
        labels = {"expired_time": "Death time"}
        help_texts = {
            "expired_time": "Leave this field as blank if the patient is alive"
        }
        widgets = {
            "date_of_birth": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
            "expired_time": TimeInput(attrs={"type": "datetime-local"}),
        }


class PatientCreateView(CreateView):
    form_class = PatientForm
    template_name = "Patient/create.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        print(self.request.user)
        self.object.nurse = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "Patient/update.html"
    success_url = "/list/patient"


class PatientDetailView(DetailView):
    model = Patient
    template_name = "Patient/detail.html"


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = "Patient/delete.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)