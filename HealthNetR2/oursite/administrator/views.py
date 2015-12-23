from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from administrator.templatetags.user_tags import is_administrator
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from healthnet.models import UserProfile, Transfer
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import logging
from doctor.forms import TransferForm

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def index(request):
    return render(request, 'administrator/admin_index.html', {})

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def create_doctor(request, first=True):

    if request.method == 'POST' and first:
        form = DoctorForm(data=request.POST)
        profile_form = DoctorProfileForm(data=request.POST)
        print("INSIDE")
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            #adds user to group
            group = Group.objects.get(name='Doctor')
            user.groups.add(group)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            profile.hospital = profile_form.cleaned_data['hospital']
            profile.save()
            return HttpResponseRedirect("/healthnet/admin/")
        else:
            print(form.errors, profile_form.errors)

    else:
        form = DoctorForm()
        profile_form = DoctorProfileForm()
    context = {"chosen" : 1, "form" : form, "profile_form" : profile_form}
    return render(request, 'administrator/admin_create_user.html', context)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def create_staff(request,first=True):

    print("CREATE staff", first)
    if request.method == 'POST' and first:
        form = StaffForm(data=request.POST)
        profile_form = StaffProfileForm(data=request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            #adds user to group
            group = Group.objects.get(name=form.cleaned_data['group'].name)
            user.groups.add(group)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.hospital = profile_form.cleaned_data['hospital']
            profile.save()
            return HttpResponseRedirect("/healthnet/admin/")
        else:
            print(form.errors, profile_form.errors)
    else:
        form = StaffForm()
        profile_form = StaffProfileForm()

    context = {"chosen" : 2, "form" : form, "profile_form" : profile_form}
    return render(request, 'administrator/admin_create_user.html', context)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def create_user(request):

    print(request.POST)
    if request.method == 'POST':
        if request.POST.get("Create Doctor","") != "":
            return create_doctor(request,False)
        elif request.POST.get("Create Staff","") != "":
            return create_staff(request,False)
        elif request.POST.get("1","") != "":
            return create_doctor(request,True)
        elif request.POST.get("2","") != "":
            return create_staff(request,True)
    chosen = 0
    context = {"chosen" : chosen}
    return render(request, 'administrator/admin_create_user.html', context)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def edit_user(request):
    user_group = "None"
    cantransfer = False
    if request.method == 'POST' and User.objects.filter(username=request.POST.get("username")):
        selected = request.POST.get("username")

        user_selected = User.objects.get(username=selected)
        admin_form = AdminEditForm(data=request.POST,instance=user_selected)

        if admin_form.is_valid():
            user = admin_form.save()
            if len(user.password) < 30:
                print(user.password)
                user.set_password(user.password)
            user.save()
            admin_form = AdminEditForm()
        else:
            print(admin_form.errors)
    else:
        admin_form = AdminEditForm()

    if request.method == "POST":
        if 'transfer' in request.POST:
            selected = request.POST.get("username")
            return HttpResponseRedirect("/healthnet/admin/transfer/%s/" % 
                User.objects.get(username=selected).id)

    #searches through All users
    search_query = request.GET.get('search_box', "")
    #filters out all users from the search and only users in groups
    users = User.objects.filter(username__regex=r"^"+search_query).filter(groups=Group.objects.all())
    users = users.order_by('username')

    selected = request.GET.get('selected_user', None)
    if selected != None:
        if "search_submit" in request.GET:
            user_selected = User.objects.get(username=selected)
            try:
                old_user = UserProfile.objects.get(user=user_selected)
                if StaffProfile.objects.get(user=request.user).hospital != old_user.hospital:
                    cantransfer = True
            except ObjectDoesNotExist:
                old_user = UserProfile()
            user_group = user_selected.groups.all()[0].name
            userProfile = old_user
            admin_form = AdminEditForm(instance=user_selected)
            #sets the initial value
        elif "delete_user" in request.GET:
            user_to_delete = User.objects.filter(username=request.GET.get("selected_user"))
            user_to_delete.delete()
    else:
        userProfile = UserProfile()

    admin_form.fields['username'].widget = forms.HiddenInput()

    context = {"admin_form" : admin_form, "users" : users, "username" : selected, 
    "user_group" : user_group, "cantransfer" :  cantransfer, "userprofile" : userProfile,}
    return render(request, 'administrator/admin_edit_user.html', context)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def log(request):
    logfile=open('log.log','r+')
    log=logfile.readlines()
    return render(request, 'administrator/admin_log.html', {"log" : log})

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def display_info(request):
    hospital_all = Hospital.objects.all()
    for e in hospital_all:
        e.admitted_patient_count = e.numberAdmittedPatients()
        e.patient_count = e.patientCount()
        e.doctor_count = e.doctorCount()
        e.staff_count = e.staffCount()
        
    context = {"hospital_all" : hospital_all}
    return render(request, 'administrator/admin_hospital_info.html', context)

@login_required
@user_passes_test(is_administrator, login_url='/healthnet/restricted/')
def transfer(request,pk):

    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST)

        if transfer_form.is_valid():
            transfer = transfer_form.save(commit=False)
            transfer.from_hospital = UserProfile.objects.get(user=User.objects.get(id=pk)).hospital.name
            transfer.user = UserProfile.objects.get(user=User.objects.get(id=pk)).user
            transfer.save()

            UserProfile.objects.get(user=User.objects.get(id=pk)).hospital = transfer.to_hospital

            logger.info("Admin \"" + request.user.username + "\" has transfered "
                " Patient \"" + transfer.user.username + "\" from Hospital : \"" +  transfer.from_hospital 
                + "\" to Hospital \"" + transfer.to_hospital.name + "\"")
            return HttpResponseRedirect("/healthnet/admin/edituser/")
        else:
            print(transfer_form.errors)
    else:
        transfer_form = TransferForm()
    tempH = StaffProfile.objects.get(user=request.user).hospital
    transfer_form.fields['to_hospital'].queryset = Hospital.objects.filter(name=tempH)

    context = {"form" : transfer_form, "patient" : User.objects.get(id=pk),}
    return render(request, 'administrator/admin_transfer_patient.html', context)