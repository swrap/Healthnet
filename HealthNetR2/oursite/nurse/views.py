from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from healthnet.models import Appointment, UserProfile, StaffProfile, DoctorProfile, Prescription, Test, PatientFile
from .forms import NurseForm, NurseProfileForm, NurseAppointmentForm
from patient.forms import PatientProfileForm, PatientForm, PatientAppointmentForm
from doctor.forms import DoctorMakeAppoitmentForm
from django.forms.models import model_to_dict
from django import forms
from nurse.templatetags.nurse_tags import *
from django.contrib.auth.decorators import login_required, user_passes_test

import logging;
import json as simplejson
import json
from django.utils.safestring import SafeString

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def index(request):
    """
    Homepage for the nurse
    :param request: Accepts a request object
    :return: The homepage of the Nurse
    """
    appointmentdic = []
    currentUser = StaffProfile.objects.get(user=request.user)
    allUserProfiles = UserProfile.objects.filter(hospital=currentUser.hospital)
    appointments = []
    for e in allUserProfiles:
        appointments += Appointment.objects.filter(user=e.user)
    for appointment in appointments:
        d = appointment.date_time
        starttime = d.strftime("%Y-%m-%dT%H:%M:%S")
        appointmentdic.append({'title': appointment.user.first_name,
                               'start': starttime
                               })

    context = {"allAppointments": SafeString(simplejson.dumps(appointmentdic))}
    return render(request, 'nurse/nurse_index.html', context)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def edit_Profile(request):
    """
    Allows the nurse to edit their profile.
    :param request: Accepts a request object
    :return: Page allowing the nurse to edit profile and save information
    """
    n = StaffProfile.objects.get(user=request.user)
    nurse_form = NurseProfileForm(instance=n)

    if request.method == 'POST':
        nurse_form = NurseProfileForm(data=request.POST,instance=n)
        if nurse_form.is_valid():
            nurse = nurse_form.save(commit=False)
            nurse.hospital = nurse_form.cleaned_data['hospital']
            nurse.save()
            logger.info("Nurse \"" + request.user.username + "\" has edited their profile.")
            return HttpResponseRedirect("/healthnet/nurse/editprofile/")
        else:
            print(nurse_form.errors)

    context = {"nurse_form" : nurse_form}
    return render(request, 'nurse/nurse_edit_profile.html', context)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def search_patient(request):
    """
    Nurses should be able to find a patient and view their prescription
    :param request: Accepts a request object
    :return: A patient prescription
    """
    if request.method == 'POST':
        patientname = request.POST.get('patientname')
        users_in_group = Group.objects.get(name="Patient").user_set.all()

        for patient in users_in_group:
            if patientname == patient.username:
                patientinfo = patient
                context = {"patientinfo": patientinfo}
                logger.info("Patient " + patient.username + " obtained by nurse")
                return render(request, 'nurse/nurse_display_patient.html', context)
        return render(request, 'nurse/nurse_search_patient.html', {"nopatient": "Patient does not exist"})
    else:
        return render(request,'nurse/nurse_search_patient.html', {})

@login_required 
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def all_patients(request):
    """
    Nurse will be able to view all of the patients in their hospital
    :param request: Accepts a request object
    :return: All of the patients in the system
    """
    if request.method == 'GET':
        if 'patientname' in request.GET:
            patient = request.GET.get('patientname')
            user = User.objects.filter(username=patient)
            if user.exists() and user[0].groups.filter(name="Patient"):
                userProfile = UserProfile.objects.filter(user=user)[0]
                pkofuserprofile = userProfile.id
                return view_patient(request,pkofuserprofile)
        if 'home' in request.GET:
            print("HERE")
            return HttpResponseRedirect("/healthnet/nurse/")

        allP = UserProfile.objects.all()
        length = int(allP.count())
    context = {"allp" : allP, "len" : length}
    return render(request, 'nurse/nurse_view_all_patients.html', context)


@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def view_patient(request,pk):
    """
    Nurse will be able to view a specific patient medical information
    :param request: Accepts a request object
    :return: The medical information for a specific user
    """
    userProfile = UserProfile.objects.get(id=pk)
    
    prescriptions = Prescription.objects.filter(user=userProfile.user)
    plen = int(prescriptions.count())

    tests = Test.objects.filter(user=userProfile.user)
    tlen = int(tests.count())

    if request.method == 'GET':
        if 'makepscript' in request.GET:
            return HttpResponseRedirect('/healthnet/nurse/makeprescription/%s/' % userProfile.id)
        elif 'maketest' in request.GET:
            return HttpResponseRedirect('/healthnet/nurse/maketest/%s/' % userProfile.id)
        elif 'update' in request.GET:
            userProfileForm = PatientProfileForm(data=request.GET,instance=userProfile)
            if userProfileForm.is_valid():
                userProfileForm.save()
            userProfile = UserProfile.objects.get(id=pk)
        elif 'allpatients' in request.GET:
            return all_patients(request)
        elif 'admitreleaseform' in request.GET:
            return admit_release_patient(request, userProfile.id)
        elif 'transferpatient' in request.GET:
            return transfer_patient(request, userProfile.id)
        elif 'viewappointments' in request.GET:
            return HttpResponseRedirect("/healthnet/nurse/viewpatientappointment/%s/" % userProfile.pk)
        elif 'home' in request.GET:
            return HttpResponseRedirect("/healthnet/nurse/")

    userForm = PatientForm(data=model_to_dict(userProfile.user))
    userProfileForm = PatientProfileForm(data=model_to_dict(userProfile))

    userProfileForm.fields['hospital'].widget = forms.HiddenInput()

    context = {"userprofile" : userProfile, "userprofileform" : userProfileForm,
    "pscripts" : prescriptions, "tests" : tests, "plen" : plen, "tlen" : tlen,
    "files" : PatientFile.objects.filter(user=userProfile.user),}
    return render(request, 'nurse/nurse_view_patient.html', context)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def admit_release_patient(request, pk):
    """
    Nurse will be able to admit or release a patient
    :param request: Accepts a request object
    :return: Returns the user information with changed admit/release status
    """
    userProfile = UserProfile.objects.get(id=pk)

    if userProfile.is_in_hospital:
        userProfile.is_in_hospital = False
        userProfile.save()
        logger.info("Nurse \"" + request.user.username + "\" has released "
            " Patient \"" + userProfile.user.username + " into " + userProfile.hospital.name + ".")
    else:
        userProfile.is_in_hospital = True
        userProfile.save()
        logger.info("Nurse \"" + request.user.username + "\" has admitted "
            " Patient \"" + userProfile.user.username + "\" out of " + userProfile.hospital.name + ".")

    return HttpResponseRedirect("/healthnet/nurse/viewpatient/%s/" % userProfile.id)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def appointments(request,pk):
    """
    Nurse will be able to view all the appointments for a specific patient
    :param request: Accepts a request object
    :param pk: Private Key of user
    :return: Returns the appointmens for that user
    """
    if request.method == 'POST':
        if 'home' in request.POST:
            return HttpResponseRedirect("/healthnet/nurse/")
        elif 'delete_all' in request.POST:
            user = UserProfile.objects.get(id=pk).user
            allAppointments = Appointment.objects.filter(user=user)
            length = int(allAppointments.count())
            allAppointments = allAppointments.delete()
            length = 0
        elif 'make' in request.POST:
            print("APP: ", UserProfile.objects.get(id=pk).user)
            return HttpResponseRedirect("/healthnet/nurse/makeappointment/%s/" % pk)
    userProfile = UserProfile.objects.get(id=pk)
    allAppointments = Appointment.objects.filter(user=userProfile.user)
    length = int(allAppointments.count())

    context = {"all_appointments" : allAppointments, "len" : length,
    "userprofile" : userProfile,}
    return render(request, 'nurse/nurse_appointment.html', context)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def delete_appointment(request, pk):
    """
    Nurse will be able to delete a specific appointment
    :param request: Accepts a request object
    :param pk: Private key of user
    :return: Return all the appointments without deleted appointment
    """
    ap = Appointment.objects.get(id=pk)
    userid = UserProfile.objects.get(user=ap.user).id
    logger.info("Nurse \"" + request.user.username + "\" has deleted his/her apointment "
                "with Patient \"" + ap.user.username + "\" at " + str(ap.date_time))
    ap.delete()
    return appointments(request, userid)

@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def edit_appointment(request, pk):
    """
    Nurse will be able to admit or release a patient
    :param request: Accepts a request object
    :param pk: Private key of user
    :return: Returns the user information with changed admit/release status
    """
    ap = Appointment.objects.get(id=pk)
    appointment_form = PatientAppointmentForm(instance=ap)

    if request.method == 'POST':
        appointment_form = PatientAppointmentForm(data=request.POST,instance=ap)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.save()
            appointment_form.save()
            logger.info("Nurse \"" + request.user.username + "\" has edited an apointment "
                "for Patient \"" + appointment.user.username + "\" at " + str(appointment.date_time))
            return appointments(request, UserProfile.objects.get(user=ap.user).id)
        else:
            print(appointment_form.errors)

    appointment_form.fields['doctor'].widget = forms.HiddenInput()

    context = {"appointment_form" : appointment_form, 'pk' : pk}
    return render(request, 'nurse/nurse_edit_appointment.html', context)


@login_required
@user_passes_test(is_nurse, login_url='/healthnet/restricted/')
def make_appointment(request,pk):
    """
    Nurse will be able to make an appointment for the user
    :param request: Accepts a request object
    :param pk: Private key of user
    :return: Returns to the apponoinments for the user
    """
    if request.method == 'POST':
        appointment_form = NurseAppointmentForm(data=request.POST)

        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.user = UserProfile.objects.get(id=pk).user
            appointment.save()

            logger.info("Nurse \"" + request.user.username + "\" has added an apointment "
                "for Patient \"" + appointment.user.username + "\" at " + str(appointment.date_time))
            return HttpResponseRedirect("/healthnet/nurse/viewpatientappointment/%s/" % pk)
        else:
            print(appointment_form.errors)
    else:
        appointment_form = NurseAppointmentForm()

    appointment_form.fields['user'].queryset = User.objects.filter(groups=Group.objects.get(name="Patient"))
    appointment_form.fields['doctor'].queryset = DoctorProfile.objects.filter(hospital=UserProfile.objects.get(id=pk).hospital)
    
    appointmentdic = []
    appointments = Appointment.objects.all()
    for appointment in appointments:
        d = appointment.date_time
        starttime = d.strftime("%Y-%m-%dT%H:%M:%S")
        appointmentdic.append({'title': appointment.user.first_name,
                               'start': starttime
                               })

    context = {"allAppointments": SafeString(simplejson.dumps(appointmentdic)),
    "appointment_form" : appointment_form, "userprofile" : UserProfile.objects.get(id=pk)}
    return render(request, 'nurse/nurse_make_appointment.html', context)