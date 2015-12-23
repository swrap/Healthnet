from django import template
from django.contrib.auth.models import User
from healthnet.models import UserProfile, PatientFile

register = template.Library()

@register.filter(name = "is_doctor")
def is_doctor(user):
	return user.is_authenticated and user.groups.filter(name='Doctor').exists()

@register.filter(name = "get_location")
def get_location(user):
	return UserProfile.objects.filter(user=user)[0].hospital.name

@register.filter(name = "extension")
def extension(patienFile):
	return PatientFile.objects.get(id=patienFile.id).extension()