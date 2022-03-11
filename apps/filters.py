from cProfile import label
import django_filters
from .models import CustomUser, Facility, Patient

CHOICES = (("ascending", "Ascending"), ("descending", "Descending"))


class FacilityFilter(django_filters.FilterSet):

    ordering = django_filters.ChoiceFilter(
        label="ordering", choices=CHOICES, method="filter_by_order"
    )

    class Meta:
        model = Facility
        fields = {
            "name": ["icontains"],
            "kind": ["exact"],
            "ward": ["exact"],
        }

    def filter_by_order(self, queryset, name, value):
        expression = "created_at" if value == "ascending" else "-created_at"
        return queryset.order_by(expression)


class CustomUserFilter(django_filters.FilterSet):

    ordering = django_filters.ChoiceFilter(
        label="ordering", choices=CHOICES, method="filter_by_order"
    )

    class Meta:
        model = CustomUser
        fields = {
            "full_name": ["icontains"],
            "role": ["exact"],
            "facility": ["exact"],
        }

    def filter_by_order(self, queryset, name, value):
        expression = "created_at" if value == "ascending" else "-created_at"
        return queryset.order_by(expression)


class PatientFilter(django_filters.FilterSet):
    ordering = django_filters.ChoiceFilter(
        label="ordering", choices=CHOICES, method="filter_by_order"
    )

    class Meta:
        model = Patient
        fields = {
            "full_name": ["icontains"],
            "ward": ["exact"],
            "facility": ["exact"],
        }

    def filter_by_order(self, queryset, name, value):
        expression = "created_at" if value == "ascending" else "-created_at"
        return queryset.order_by(expression)
