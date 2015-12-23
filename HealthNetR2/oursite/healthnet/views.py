from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from healthnet.models import Message, Hospital, StaffProfile
from healthnet.forms import MessageForm
from administrator.forms import StaffProfileForm
from django import forms
from healthnet.templatetags.healthnet_tags import *

def index(request):
    """
    Renders a request object and loads up the index page.
    :param request: Accepts a request object.
    :return: An index.html is rendered showing the homepage and provided links.
    """

    #creates the groups if they do not exist
    if not Group.objects.filter(name="Administrator").exists():
        Group.objects.create(name="Administrator")
    if not Group.objects.filter(name="Doctor").exists():
        Group.objects.create(name="Doctor")
    if not Group.objects.filter(name="Patient").exists():
        Group.objects.create(name="Patient")
    if not Group.objects.filter(name="Nurse").exists():
        Group.objects.create(name="Nurse")
    if Hospital.objects.count() == 0:
        h = Hospital(name="Chesnut Hill Hospital")
        h.save()
        h = Hospital(name="Pennsylvania Central Hospital")
        h.save()

    #adds default admin on the site, when db is cleaned
    if User.objects.filter(groups__name='Administrator').count() == 0:
        user = User.objects.create_user(username="admin",email="admin@rit.edu",password="admin",
            first_name='admin',last_name='admin')

        user.save()

        staff = StaffProfile(user=user,hospital=Hospital.objects.get(name="Chesnut Hill Hospital"),
            previous_employment="Somewhere",education_information="None what so ever", accreditation="Nothing")
        staff.save()
        
        #adds the admin to the group
        user.groups.add(Group.objects.filter(name="Administrator")[0])
        user.save()

    if request.user.is_authenticated():
        user = request.user
        user_group = user.groups.all()[0].name
        if user_group == "Administrator":
            user_group = "admin"
        return HttpResponseRedirect("/healthnet/" + user_group.lower() + "/")
    return render(request, "healthnet/index.html")

def user_logout(request):
    """
    The user is logged out of his account an returned to the homepage.
    :param request: Accepts a request object.
    :return: A user is logged out, and returned to the homepage.
    """
    # Since user is logged in, we can just log them out.
    if request.user.is_authenticated():
        logout(request)
    # Takes the user back to the index page.
    return HttpResponseRedirect("/healthnet/")

def user_login(request):
    """
    Allows a user to attempt to login with the right credentials
    :param request: Accepts a request object.
    :return: A user is logged out, and returned to the homepage.
    """
    #redirects user back to homepage
    if request.user.is_active:
        return HttpResponseRedirect("/healthnet/")

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user = request.user
                user_group = user.groups.all()[0].name
                if user_group == "Administrator":
                    user_group = "admin"
                return HttpResponseRedirect("/healthnet/" + user_group.lower() + "/")
            else:
                return render(request, 'healthnet/index.html', {"login" : "Incorrect Login Username or password"})
        else:
            return render(request, 'healthnet/index.html', {"login" : "Incorrect Login Username or password"})
    else:
        return render(request, 'healthnet/index.html', {})

@login_required
def user_messages(request):
    if request.method == 'POST' and request.user.is_authenticated():
        user = request.user
        #establish which group the user is in
        user_group = user.groups.all()[0].name
        if user_group == "Administrator":
            user_group = "admin"
        return HttpResponseRedirect("/healthnet/" + user_group.lower() + "/")

    from_messages = Message.objects.filter(from_user=request.user.username)
    to_messages = Message.objects.filter(to_user=request.user.username)
    all_messages = from_messages | to_messages

    user = User.objects.get(pk=request.user.id)
    group = user.groups.all()[0].name.lower()
    if group == "administrator":
        group = "admin"
    group += "base.html"

    context = {"all_messages" : all_messages, "group" : group}
    return render(request, 'healthnet/message.html', context)

@login_required
def user_new_message(request):
    message_form = MessageForm()
    message_form.fields['from_user'].initial = request.user.username

    if "submit" in request.POST:
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            message_form.save()
            return HttpResponseRedirect("/healthnet/messages/")
    elif "cancel" in request.POST:
        return HttpResponseRedirect("/healthnet/messages/")

    message_form.fields['date_time'].widget = forms.HiddenInput()

    user = User.objects.get(pk=request.user.id)
    group = user.groups.all()[0].name.lower()
    if group == "administrator":
        group = "admin"
    group += "base.html"

    context = {"message_form": message_form, "group" : group}
    return render(request, 'healthnet/new_message.html', context)

def restricted(request):
    if request.user.is_authenticated:
        context = {"message" : "Access Restricted"}
    else:
        context = {"message" : "Login Required"}
    return render(request, 'healthnet/restricted.html', context)