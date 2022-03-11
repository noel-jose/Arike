from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import CustomUser, Patient, VisitSchedule
from datetime import timedelta
from arike.settings import EMAIL_HOST_USER

from arike.celery import app


from datetime import datetime
import pytz


@app.task
def send_mail_reminder():
    print("==================================================!")
    current_time = datetime.now(pytz.timezone("UTC"))
    print("Current time " + str(current_time))
    for user in CustomUser.objects.filter(schedule_alert_time__lt=current_time):
        patients_assigned = Patient.objects.filter(deleted=False, nurse=user)
        visits_scheduled = VisitSchedule.objects.filter(
            deleted=False, nurse=user, cancelled=False, date_time__gt=current_time
        )
        email_content = f"""You have,
            {patients_assigned.count()} Patients Assinged to you.
            {visits_scheduled.count()} Visits scheduled.
        """
        send_mail(
            "Daily Report from Arike",
            email_content,
            EMAIL_HOST_USER,
            [user.email],
        )
        user.scheduled_alert_time = user.scheduled_alert_time + timedelta(days=1)
        user.save(update_fields=["user.scheduled_alert_time"])
        print(f"Sent mail to  {user}")


app.conf.beat_schedule = {
    "send-every-300-seconds": {
        "task": "apps.tasks.send_mail_reminder",
        "schedule": 300.0,
    },
}
