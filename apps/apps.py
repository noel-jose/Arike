from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps"

    def ready(self):
        from .signals import send_login_mail, send_treatment_report
