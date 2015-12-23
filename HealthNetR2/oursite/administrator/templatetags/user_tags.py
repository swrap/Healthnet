from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name = "is_administrators")
def is_administrator(user):
	return user.is_authenticated and user.groups.filter(name='Administrator').exists()

@register.assignment_tag(name = "all_users")
def all_users(s):
	users = User.objects.filter(name__regex=s)
	groups = Group.objects.all()
	for e in groups:
		print(e.name)
		users = users.groups.filter(name=e.name)
	return users