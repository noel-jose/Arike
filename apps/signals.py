from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from arike.settings import EMAIL_HOST_USER, ALLOWED_HOSTS

from .models import CustomUser, FamilyDetail, Treatment


# sending a mail to the user when account is created
def send_login_mail(instance):
    receiver_email = instance.email
    subject = instance.full_name + " Login Details to arike"
    content = f"""
    Welcome to Arike.
    Your login details are as follows
    User name : "{instance.username}"
    Password : "welcometoarike"
    Login to : { ALLOWED_HOSTS }
    Do change the password after you login
    """
    send_mail(subject, content, EMAIL_HOST_USER, [receiver_email])
    print(f"Login mail has been successfully sent to { instance.username }")


# sending mail to family members when treatment is updated for user
@receiver(post_save, sender=Treatment)
def send_treatment_report(sender, instance, created, **kwargs):
    print("Entered treatment report")

    user = instance.patient
    content = f"""
    The treatment Details of {user } has been updated.
    Care type : {instance.care_type}
    Care Sub type : { instance.care_sub_type}
    Description : { instance.description }
    """
    subject = f"{user} treatment update"
    familys = FamilyDetail.objects.filter(deleted=False, patient=user)
    emails = []
    for family in familys:
        emails.append(family.email)
    send_mail(subject, content, EMAIL_HOST_USER, emails)
    print("Successfully sent treatment updates")
