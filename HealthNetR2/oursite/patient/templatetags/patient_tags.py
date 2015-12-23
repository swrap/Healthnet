from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name = "is_patient")
def is_patient(user):
	return user.is_authenticated and user.groups.filter(name='Patient').exists()