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
from django.contrib.auth.views import LogoutView

from apps.views import (
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
    UserUpdateView,
    UsersCreateView,
    UsersListView,
    UserLoginView,
    UserDetailView,
    UserDeleteView,
    FacilityListView,
    FacilityCreateView,
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
]
