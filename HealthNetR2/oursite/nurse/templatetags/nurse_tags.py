from django import template
from django.contrib.auth.models import User
from healthnet.models import UserProfile

register = template.Library()


@register.filter(name="is_nurse")
def is_nurse(user):
    return user.is_authenticated and user.groups.filter(name='Nurse').exists()

@register.filter(name = "get_location")
def get_location(user):
	return UserProfile.objects.filter(user=user)[0].hospital.name