from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from base import email

User= get_user_model()


@receiver(post_save, sender=User)
def notfiy_user_created(sender, instance, created, **kwargs):
    if created:
        email.send_welcome_email(instance.email)
    else:
        print(f"User updated: {instance.email}")