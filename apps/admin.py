from django.contrib import admin

# Register your models here.

from apps.models import (
    CustomUser,
    State,
    District,
    Lsgbody,
    Ward,
    Facility,
    Patient,
    Disease,
    FamilyDetail,
    Treatment,
    TreatmentNotes,
)

admin.sites.site.register(CustomUser)
admin.sites.site.register(State)
admin.sites.site.register(District)
admin.sites.site.register(Lsgbody)
admin.sites.site.register(Ward)
admin.sites.site.register(Facility)
admin.sites.site.register(Patient)
admin.sites.site.register(FamilyDetail)
