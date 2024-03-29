"""arike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.contrib.auth.views import LogoutView, PasswordChangeView


from apps.views import (
    Dashboard,
    NewPasswordChangeView,
    DieseaseHistoryCreateView,
    DiseaseHistoryDeleteView,
    DiseaseHistoryListView,
    DiseaseHistoryUpdateView,
    FacilityDeleteView,
    FacilityDetailView,
    FacilityUpdateView,
    FamilyCreateView,
    FamilyDeleteView,
    FamilyListView,
    FamilyUpdateView,
    PatientCreateView,
    PatientDeleteView,
    PatientDetailView,
    PatientListView,
    PatientUpdateView,
    TreatmentCreateView,
    TreatmentDeleteView,
    TreatmentListView,
    TreatmentUpdateView,
    UserUpdateView,
    UsersCreateView,
    UsersListView,
    UserLoginView,
    UserDetailView,
    UserDeleteView,
    FacilityListView,
    FacilityCreateView,
    VisitDetailsCreateView,
    VisitDetailsListView,
    VisitDetailsUpdateView,
    VisitDetailsDeleteView,
    VisitScheduleCreateView,
    VisitScheduleListView,
    VisitScheduleUpdateView,
    VisitScheduleDeleteView,
    TreatmentNotesCreateView,
    TreatmentNotesListView,
    TreatmentNotesUpdateView,
    TreatmentNotesDeleteView,
    ReferView,
    VisitDetailsListPatientView,
    TreatmentNotesVisitCreateView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("login", UserLoginView.as_view()),
    path("logout", LogoutView.as_view()),
    # urls for distadmin user views
    path("list/users", UsersListView.as_view()),
    path("create/user", UsersCreateView.as_view()),
    path("update/user/<pk>", UserUpdateView.as_view()),
    path("detail/user/<pk>", UserDetailView.as_view()),
    path("delete/user/<pk>", UserDeleteView.as_view()),
    # urls for distadmin facility views
    path("list/facility", FacilityListView.as_view()),
    path("create/facility", FacilityCreateView.as_view()),
    path("update/facility/<pk>", FacilityUpdateView.as_view()),
    path("detail/facility/<pk>", FacilityDetailView.as_view()),
    path("delete/facility/<pk>", FacilityDeleteView.as_view()),
    # urls for patient views
    path("list/patient", PatientListView.as_view()),
    path("create/patient", PatientCreateView.as_view()),
    path("update/patient/<pk>", PatientUpdateView.as_view()),
    path("detail/patient/<pk>", PatientDetailView.as_view()),
    path("delete/patient/<pk>", PatientDeleteView.as_view()),
    # urls for family detail views
    path("create/family/<int:patient_id>", FamilyCreateView.as_view()),
    path("list/family/<int:patient_id>", FamilyListView.as_view()),
    path("update/family/<pk>", FamilyUpdateView.as_view()),
    path("delete/family/<pk>", FamilyDeleteView.as_view()),
    # urls for the treatment views
    path("create/treatment/<int:patient_id>", TreatmentCreateView.as_view()),
    path("list/treatment/<int:patient_id>", TreatmentListView.as_view()),
    path("update/treatment/<pk>", TreatmentUpdateView.as_view()),
    path("delete/treatment/<pk>", TreatmentDeleteView.as_view()),
    # urls for the disease history views
    path("create/diseasehistory/<int:patient_id>", DieseaseHistoryCreateView.as_view()),
    path("list/diseasehistory/<int:patient_id>", DiseaseHistoryListView.as_view()),
    path("update/diseasehistory/<pk>", DiseaseHistoryUpdateView.as_view()),
    path("delete/diseasehistory/<pk>", DiseaseHistoryDeleteView.as_view()),
    # urls for the visit schedule
    path("create/visitschedule", VisitScheduleCreateView.as_view()),
    path("list/visitschedule", VisitScheduleListView.as_view()),
    path("update/visitschedule/<pk>", VisitScheduleUpdateView.as_view()),
    path("delete/visitschedule/<pk>", VisitScheduleDeleteView.as_view()),
    # urls for the visit details
    path(
        "create/visitdetails/<int:visit_schedule_id>", VisitDetailsCreateView.as_view()
    ),
    path("list/visitdetails/<int:visit_schedule_id>", VisitDetailsListView.as_view()),
    path("update/visitdetails/<pk>", VisitDetailsUpdateView.as_view()),
    path("delete/visitdetails/<pk>", VisitDetailsDeleteView.as_view()),
    # urls for the treatment notes
    path(
        "create/treatmentnote/<int:treatment_id>",
        TreatmentNotesCreateView.as_view(),
    ),
    path(
        "list/treatmentnote/<int:treatment_id>",
        TreatmentNotesListView.as_view(),
    ),
    path(
        "update/treatmentnote/<pk>",
        TreatmentNotesUpdateView.as_view(),
    ),
    path(
        "delete/treatmentnote/<pk>",
        TreatmentNotesDeleteView.as_view(),
    ),
    # url for passowrd reset view
    path("resetpassword", NewPasswordChangeView.as_view()),
    # url for patient refer
    path("refer/patient/<int:patient_id>", ReferView.as_view()),
    path("", Dashboard.as_view()),
    path(
        "list/visitdetailspatient/<int:patient_id>",
        VisitDetailsListPatientView.as_view(),
    ),
    path(
        "list/visittreatmentnotes/<int:visit_schedule_id>",
        TreatmentNotesVisitCreateView.as_view(),
    ),
]
