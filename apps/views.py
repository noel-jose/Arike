from .signals import send_login_mail
from django.contrib.auth import views
from django.views import View
from django.shortcuts import render
import logging

from .models import (
    CustomUser,
    Facility,
    FamilyDetail,
    Patient,
    Treatment,
    DiseaseHistory,
    TreatmentNotes,
    VisitSchedule,
    VisitDetails,
)

from .filters import CustomUserFilter, FacilityFilter, PatientFilter
from django_filters.views import FilterView

from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash

# Create your views here.


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms import ChoiceField, ModelForm, TimeInput
from django import forms

from .models import FACILITY_KIND, GENDER_CHOICES

from .Mixin import UserPermissionMixin

from django.contrib.auth.views import PasswordChangeView


class NewPasswordChangeView(PasswordChangeView):
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        self.object.is_verified = True
        return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        if self.request.user.is_verified == True:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect("/resetpassword")


"""

    Creating views for Custom user

"""


class UsersListView(LoginRequiredMixin, UserPermissionMixin, FilterView):
    permission_required = "Secondary Nurse", "District Admin"

    template_name = "User/customuser_list.html"
    context_object_name = "users"
    filterset_class = CustomUserFilter

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
            "phone",
            "role",
            "district",
            "facility",
            "schedule_alert_time",
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
        widgets = {
            "schedule_alert_time": TimeInput(attrs={"type": "datetime-local"}),
        }


class UsersCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin"

    form_class = CustomUserForm
    template_name = "User/customuser_create.html"
    success_url = "/"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.set_password("welcometoarike")
        print(self.object.password)
        self.object.save()
        send_login_mail(self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = CustomUser
    form_class = CustomUserForm
    template_name = "User/customuser_update.html"
    success_url = "/"


class UserDetailView(LoginRequiredMixin, UserPermissionMixin, DetailView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"
    model = CustomUser
    template_name = "User/customuser_detail.html"


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin"

    model = CustomUser
    template_name = "User/customuser_delete.html"
    success_url = "/"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


""" 

    Creating Views for Facilities 

"""


class FacilityListView(LoginRequiredMixin, UserPermissionMixin, FilterView):
    permission_required = "District Admin"

    template_name = "Facility/list.html"
    context_object_name = "facilities"
    filterset_class = FacilityFilter

    def get_queryset(self):
        facilities = Facility.objects.filter(deleted=False)
        return facilities


class FacilityForm(ModelForm):
    kind = forms.ChoiceField(choices=FACILITY_KIND, widget=forms.RadioSelect)

    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "pincode", "phone", "ward"]


class FacilityCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin"

    form_class = FacilityForm
    template_name = "Facility/create.html"
    success_url = "/list/facility"


class FacilityUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin"

    model = Facility
    form_class = FacilityForm
    template_name = "Facility/update.html"
    success_url = "/list/facility"


class FacilityDetailView(LoginRequiredMixin, UserPermissionMixin, DetailView):
    permission_required = "District Admin"

    model = Facility
    template_name = "Facility/detail.html"


class FacilityDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin"

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


class PatientListView(LoginRequiredMixin, UserPermissionMixin, FilterView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Patient
    template_name = "Patient/list.html"
    context_object_name = "patients"
    filterset_class = PatientFilter

    def get_queryset(self):
        if self.request.user.role == "District Admin":
            patients = Patient.objects.filter(
                deleted=False,
            )
        else:
            patients = Patient.objects.filter(
                deleted=False, facility=self.request.user.facility
            )
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
            "facility",
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


class PatientCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

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


class PatientUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Patient
    form_class = PatientForm
    template_name = "Patient/update.html"
    success_url = "/list/patient"


class PatientDetailView(LoginRequiredMixin, UserPermissionMixin, DetailView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Patient
    template_name = "Patient/detail.html"


class PatientDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Patient
    template_name = "Patient/delete.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


"""

        Creating views for Family Details

"""


class FamilyForm(ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = FamilyDetail
        fields = [
            "full_name",
            "date_of_birth",
            "phone",
            "email",
            "address",
            "relation",
            "gender",
            "education",
            "occupation",
            "remarks",
            "is_primary",
        ]
        labels = {"is_primary": "Primary contact for Patient"}
        widgets = {
            "date_of_birth": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }


class FamilyCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = FamilyDetail
    form_class = FamilyForm
    template_name = "FamilyDetails/create.html"
    success_url = "/"

    # def get_context_data(self, **kwargs):
    #     context = super(FamilyCreateView, self).get_context_data(**kwargs)
    #     context["patient_id"] = self.kwargs["patient_id"]
    #     return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        patient_id = self.kwargs["patient_id"]
        patient = Patient.objects.get(pk=patient_id)
        self.object.patient = patient
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FamilyListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = FamilyDetail
    template_name = "FamilyDetails/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        print(patient_id)
        patient = Patient.objects.get(pk=patient_id)
        objects = FamilyDetail.objects.filter(deleted=False, patient=patient)
        print(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_id"] = self.kwargs["patient_id"]
        return context


class FamilyUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = FamilyDetail
    form_class = FamilyForm
    template_name = "FamilyDetails/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FamilyDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = FamilyDetail
    template_name = "FamilyDetails/delete.html"
    success_url = "/list/family"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


""""

    Creating Treatment views  

"""


class TreatmentForm(ModelForm):
    class Meta:
        model = Treatment
        fields = ["care_type", "description", "care_sub_type", "active"]


class TreatmentCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Treatment
    form_class = TreatmentForm
    template_name = "Treatment/create.html"
    success_url = "/list/treatment"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        patient_id = self.kwargs["patient_id"]
        patient = Patient.objects.get(pk=patient_id)
        self.object.patient = patient
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            patient_id = self.kwargs["patient_id"]
            return self.success_url + "/" + str(patient_id)


class TreatmentListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Treatment
    template_name = "Treatment/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        patient = Patient.objects.get(pk=patient_id)
        objects = Treatment.objects.filter(deleted=False, patient=patient).order_by(
            "-updated_at"
        )
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_id"] = self.kwargs["patient_id"]
        context["patient"] = Patient.objects.get(pk=self.kwargs["patient_id"]).full_name
        context["nurse"] = Patient.objects.get(pk=self.kwargs["patient_id"]).nurse
        return context


class TreatmentUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Treatment
    form_class = TreatmentForm
    template_name = "Treatment/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TreatmentDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = Treatment
    template_name = "Treatment/delete.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


"""

    Views for Disease History 

"""


class DiseaseHistoryForm(ModelForm):
    class Meta:
        model = DiseaseHistory
        fields = ["name", "icds_code", "description"]


class DieseaseHistoryCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = DiseaseHistory
    form_class = DiseaseHistoryForm
    template_name = "DiseaseHistory/create.html"
    success_url = "/list/diseasehistory"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        patient_id = self.kwargs["patient_id"]
        patient = Patient.objects.get(pk=patient_id)
        self.object.patient = patient
        self.object.treated_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            patient_id = self.kwargs["patient_id"]
            return self.success_url + "/" + str(patient_id)


class DiseaseHistoryListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = DiseaseHistory
    template_name = "DiseaseHistory/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        patient = Patient.objects.get(pk=patient_id)
        objects = DiseaseHistory.objects.filter(
            deleted=False, patient=patient
        ).order_by("-updated_at")
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_id"] = self.kwargs["patient_id"]
        context["patient"] = Patient.objects.get(pk=self.kwargs["patient_id"])
        return context


class DiseaseHistoryUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = DiseaseHistory
    form_class = DiseaseHistoryForm
    template_name = "DiseaseHistory/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DiseaseHistoryDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = DiseaseHistory
    template_name = "DiseaseHistory/delete.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


"""

    Visit Schedule views


"""


class VisitScheduleForm(ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.filter(deleted=False))

    class Meta:
        model = VisitSchedule
        fields = ["date_time", "duration", "patient"]

        widgets = {
            "date_time": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }


class VisitScheduleCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = "VisitSchedule/create.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.nurse = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VisitScheduleListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitSchedule
    template_name = "VisitSchedule/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        objects = VisitSchedule.objects.filter(
            deleted=False, nurse=self.request.user
        ).order_by("-updated_at")
        return objects


class VisitScheduleUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = "VisitSchedule/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VisitScheduleDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitSchedule
    template_name = "VisitSchedule/delete.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


""""

    Visit Detail Views

"""


class VisitDetailsForm(ModelForm):
    class Meta:
        model = VisitDetails
        fields = [
            "pallative_phase",
            "blood_pressure",
            "pulse",
            "General_Random_Blood_Sugar",
            "Personal_hygiene",
            "Mouth_hygiene",
            "Public_hygiene",
            "systematic_examination",
            "notes",
            "patient_at_peace",
            "pain",
            "symptoms",
        ]


class VisitDetailsCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitDetails
    form_class = VisitDetailsForm
    template_name = "VisitDetails/create.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        visit_schedule_id = self.kwargs["visit_schedule_id"]
        visitschedule = VisitSchedule.objects.get(pk=visit_schedule_id)
        self.object.visit_schedule = visitschedule
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            return self.success_url


class VisitDetailsListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitDetails
    template_name = "VisitDetails/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        visit_schedule_id = self.kwargs["visit_schedule_id"]
        visitschedule = VisitSchedule.objects.get(pk=visit_schedule_id)
        objects = VisitDetails.objects.filter(
            deleted=False, visit_schedule=visitschedule
        ).order_by("-updated_at")
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visitschedule"] = VisitSchedule.objects.get(
            pk=self.kwargs["visit_schedule_id"]
        )
        return context


class VisitDetailsUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitDetails
    form_class = VisitDetailsForm
    template_name = "VisitDetails/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VisitDetailsDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = VisitDetails
    template_name = "VisitDetails/delete.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


"""

    Creating views for Treatement notes model

"""


class TreatmentNotesForm(ModelForm):
    class Meta:
        model = TreatmentNotes
        fields = ["heading", "description"]


class TreatmentNotesCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = TreatmentNotes
    form_class = TreatmentNotesForm
    template_name = "TreatmentNotes/create.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        treatment_id = self.kwargs["treatment_id"]
        treatment = Treatment.objects.get(pk=treatment_id)
        self.object.treatment = treatment
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TreatmentNotesListView(LoginRequiredMixin, UserPermissionMixin, ListView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = TreatmentNotes
    template_name = "TreatmentNotes/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        treatment_id = self.kwargs["treatment_id"]
        treatment = Treatment.objects.get(pk=treatment_id)
        objects = TreatmentNotes.objects.filter(
            deleted=False, treatment=treatment
        ).order_by("-updated_at")
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["treatment"] = Treatment.objects.get(pk=self.kwargs["treatment_id"])
        return context


class TreatmentNotesUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = TreatmentNotes
    form_class = TreatmentNotesForm
    template_name = "TreatmentNotes/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TreatmentNotesDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = TreatmentNotes
    template_name = "TreatmentNotes/delete.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


###
###
###     View for a PHC to refer to a CHC
###
###
class ReferForm(forms.Form):
    secondary_nurse = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(deleted=False, role="Secondary Nurse")
    )


class ReferView(LoginRequiredMixin, UserPermissionMixin, View):
    permission_required = "District Admin", "Primary Nurse"

    form_class = ReferForm
    template = "Patient/refer.html"

    def get(self, request, patient_id):
        try:
            form = self.form_class()
            return render(request, self.template, {"form": form})

        except Exception as e:
            logging.error(e)
            return HttpResponseRedirect("/500")

    def post(self, request, patient_id):

        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            phc_nurse = self.request.user
            patient_id = self.kwargs["patient_id"]
            patient = Patient.objects.get(pk=patient_id)
            secondary_nurse_id = form.data["secondary_nurse"]
            secondary_nurse = CustomUser.objects.get(pk=secondary_nurse_id)
            patient.nurse = secondary_nurse
            patient.facility = secondary_nurse.facility
            patient.save()
            return HttpResponseRedirect("/list/patient")
        return render(request, self.template, {"form": form})


##
##
## view for dashboard
##
##


class Dashboard(LoginRequiredMixin, UserPermissionMixin, View):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"
    template = "dashboard.html"

    def get(self, request):
        return render(request, self.template)
