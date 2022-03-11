from .signals import send_login_mail
from django.contrib.auth import views

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
            "password",
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


class UsersCreateView(LoginRequiredMixin, UserPermissionMixin, CreateView):
    permission_required = "District Admin"

    form_class = CustomUserForm
    template_name = "User/customuser_create.html"
    success_url = "/login"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        send_login_mail(self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"

    model = CustomUser
    form_class = CustomUserForm
    template_name = "User/customuser_update.html"
    success_url = "/dashboard"


class UserDetailView(LoginRequiredMixin, UserPermissionMixin, DetailView):
    permission_required = "District Admin", "Primary Nurse", "Secondary Nurse"
    model = CustomUser
    template_name = "User/customuser_detail.html"


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    permission_required = "District Admin"

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


class PatientListView(FilterView):
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


class FamilyCreateView(CreateView):
    model = FamilyDetail
    form_class = FamilyForm
    template_name = "FamilyDetails/create.html"
    success_url = "/dashboard"

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


class FamilyListView(ListView):
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


class FamilyUpdateView(UpdateView):
    model = FamilyDetail
    form_class = FamilyForm
    template_name = "FamilyDetails/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FamilyDeleteView(DeleteView):
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


class TreatmentCreateView(CreateView):
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


class TreatmentListView(ListView):
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


class TreatmentUpdateView(UpdateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = "Treatment/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TreatmentDeleteView(DeleteView):
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


class DieseaseHistoryCreateView(CreateView):
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


class DiseaseHistoryListView(ListView):
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


class DiseaseHistoryUpdateView(UpdateView):
    model = DiseaseHistory
    form_class = DiseaseHistoryForm
    template_name = "DiseaseHistory/update.html"
    success_url = "/list/patient"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DiseaseHistoryDeleteView(DeleteView):
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


class VisitScheduleCreateView(CreateView):
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


class VisitScheduleListView(ListView):
    model = VisitSchedule
    template_name = "VisitSchedule/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        objects = VisitSchedule.objects.filter(
            deleted=False, nurse=self.request.user
        ).order_by("-updated_at")
        return objects


class VisitScheduleUpdateView(UpdateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = "VisitSchedule/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VisitScheduleDeleteView(DeleteView):
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


class VisitDetailsCreateView(CreateView):
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


class VisitDetailsListView(ListView):
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


class VisitDetailsUpdateView(UpdateView):
    model = VisitDetails
    form_class = VisitDetailsForm
    template_name = "VisitDetails/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VisitDetailsDeleteView(DeleteView):
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


class TreatmentNotesCreateView(CreateView):
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


class TreatmentNotesListView(ListView):
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


class TreatmentNotesUpdateView(UpdateView):
    model = TreatmentNotes
    form_class = TreatmentNotesForm
    template_name = "TreatmentNotes/update.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TreatmentNotesDeleteView(DeleteView):
    model = TreatmentNotes
    template_name = "TreatmentNotes/delete.html"
    success_url = "/list/visitschedule"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
