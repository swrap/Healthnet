from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from patient.templatetags.patient_tags import *
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from healthnet.models import UserProfile, Appointment, Prescription, Test, PatientFile
from django import forms
from django.core import serializers
from django.forms.models import model_to_dict
import logging;
import json as simplejson
import json
from django.utils.safestring import SafeString

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def index(request):
    """
    Homepage for the patient
    :param request: Accepts a request object
    :return: The homepage of the Nurse
    """
    appointmentdic = []
    currentUser = UserProfile.objects.get(user=request.user)
    allUserProfiles = UserProfile.objects.filter(hospital=currentUser.hospital)
    appointments = []
    for e in allUserProfiles:
        appointments += Appointment.objects.filter(user=e.user)
    for appointment in appointments: 
        d = appointment.date_time
        starttime = d.strftime("%Y-%m-%dT%H:%M:%S")
        if request.user.username == appointment.user.username:
            appointmentdic.append({'title': appointment.user.first_name,
                                   'start': starttime
                                   })
        else:
            appointmentdic.append({'title':"Dr " + appointment.doctor.user.first_name,
                                    'start':starttime
                                   })
    context = {"allAppointments": SafeString(simplejson.dumps(appointmentdic))}
    return render(request, 'patient/patient_index.html', context)

def register(request):
    """
    Allows new patients to register
    :param request: Accepts a request object
    :return: Page allowing the patients to register in the system
    """
    if request.method == 'POST':
        patient_form = PatientForm(data=request.POST)
        patient_profile_form = PatientProfileForm(data=request.POST)

        if patient_form.is_valid() and patient_profile_form.is_valid():
            user = patient_form.save()
            user.set_password(user.password)
            #adds user to group
            #pulls the cleaned data of the group choice
            group = Group.objects.get(name="Patient")
            user.groups.add(group)
            user.save()

            profile = patient_profile_form.save(commit=False)
            profile.user = user
            profile.save()
            logger.info("User \"" + user.username + "\" has been registered")
            return HttpResponseRedirect("/healthnet/")
        else:
            print(patient_form.errors, patient_profile_form.errors)

    else:
        patient_form = PatientForm()
        patient_profile_form = PatientProfileForm()

    context = {"patient_form" : patient_form, "patient_profile_form" : patient_profile_form}
    return render(request, 'patient/patient_register.html', context)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def edit_patient(request):
    """
    Patient can edit their profile. Also allows the patient
    to export their data.
    :param request: Accepts a request object
    :return: Page allowing the patient to edit profile and save information
    """
    if request.method == 'POST':
        #used to export the data if clicked on
        if 'export' in request.POST:
            import csv
            from django.utils.encoding import smart_str
            userProfile = UserProfile.objects.get(user=request.user)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = str("attachment; filename=" + 
                userProfile.user.first_name + "_" +
                userProfile.user.last_name + "_Profile_Information.csv")
            writer = csv.writer(response, csv.excel)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"Username"),
                smart_str(userProfile.user.username)
            ])
            writer.writerow([
                smart_str(u"First Name"),
                smart_str(userProfile.user.first_name)
            ])
            writer.writerow([
                smart_str(u"Last Name"),
                smart_str(userProfile.user.last_name)
            ])
            writer.writerow([
                smart_str(u"Age"),
                smart_str(userProfile.age)
            ])
            writer.writerow([
                smart_str(u"Date of Birth"),
                smart_str(userProfile.date_of_birth)
            ])
            writer.writerow([
                smart_str(u"Spouse First Name"),
                smart_str(userProfile.spouse_first_name)
            ])
            writer.writerow([
                smart_str(u"Next of Kin"),
                smart_str(userProfile.next_of_kin)
            ])
            writer.writerow([
                smart_str(u"Emergency Contact"),
                smart_str(userProfile.emergency_contact)
            ])
            writer.writerow([
                smart_str(u"Phone Number"),
                smart_str(userProfile.phone_number)
            ])
            writer.writerow([
                smart_str(u"Sex"),
                smart_str(userProfile.sex)
            ])
            writer.writerow([
                smart_str(u"Weight"),
                smart_str(userProfile.weight)
            ])
            writer.writerow([
                smart_str(u"Height"),
                smart_str(userProfile.height)
            ])
            writer.writerow([
                smart_str(u"Insurance"),
                smart_str(userProfile.insurance)
            ])
            writer.writerow([
                smart_str(u"Hospital"),
                smart_str(userProfile.hospital.name)
            ])
            return response
        else:
            #else it assumes that the patient is updating their data
            patient_form = PatientForm(data=request.POST,instance=request.user)
            patient_form.fields['password'].required = False
            patient_profile_form = PatientEditProfileForm(instance=UserProfile.objects.filter(user=request.user)[0],data=request.POST)
            if patient_form.is_valid() and patient_profile_form.is_valid():
                user = patient_form.save()
                user.save()

                profile = patient_profile_form.save(commit=False)
                profile.user = user
                profile.save()

                logger.info("Patient \"" + user.username + "\" has edited his/her info")
                return HttpResponseRedirect("/healthnet/patient/")
            else:
                print(patient_form.errors, patient_profile_form.errors)
    else:
        patient_form = PatientForm(instance=request.user)
        patient_profile_form = PatientEditProfileForm(instance=UserProfile.objects.filter(user=request.user)[0])

    patient_form.fields['username'].widget = forms.HiddenInput()
    patient_form.fields['password'].required = False

    context = {"patient_form" : patient_form, "patient_profile_form" : patient_profile_form}
    return render(request, 'patient/patient_edit_patient.html', context)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def make_appointment(request):
    """
    Patient should be able to create or update an appointment with a doctor and at one of the doctor's
    available location
    :param request: Accepts a request object
    :return: An appointment
    """
    if request.method == 'POST':
        #sets up the doctor for the appointment
        appointment_form = PatientAppointmentForm(data=request.POST)

        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            logger.info("Patient \"" + appointment.user.username + "\" has added an apointment "
                "with Doctor " + appointment.doctor.user.username + " at " + str(appointment.date_time))
            return HttpResponseRedirect("/healthnet/patient/appointments/")
        else:
            print(appointment_form.errors)
    else:
        appointment_form = PatientAppointmentForm()
    h = UserProfile.objects.get(user=request.user).hospital
    dp = DoctorProfile.objects.filter(hospital=h)
    appointment_form.fields['doctor'].queryset = dp

    context = {"appointment_form" : appointment_form}
    return render(request, 'patient/patient_make_appointment.html', context)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def appointments(request):
    """
    Patient views all of the avaiable appointments
    :param request: Accepts a request object
    :return: All appointments for that user
    """
    appointments = Appointment.objects.all()
    appointments = appointments.filter(user=request.user)
    if request.method == 'POST':
        if 'home' in request.POST:
            return HttpResponseRedirect("/healthnet/patient/")
        elif 'delete_all' in request.POST:
            appointments = appointments.delete()
        elif 'make' in request.POST:
            return HttpResponseRedirect("/healthnet/patient/makeappointment/")

    allAppointments = Appointment.objects.filter(user=request.user)
    context = {"all_appointments" : allAppointments, "len" : allAppointments.count(),
    "location" : UserProfile.objects.get(user=request.user).hospital,}
    return render(request, 'patient/patient_appointment.html', context)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def edit_appointment(request, pk):
    """
    Patient will be able to edit their appointments
    :param request: Accepts a request object
    :return: Appointment form with filled in data
    """
    ap = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment_form = PatientAppointmentForm(data=request.POST,instance=ap)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.user = request.user

            appointment.save()
            appointment_form.save()
            logger.info("Patient \"" + appointment.user.username + "\" has edited his/her apointment "
                "with Doctor " + appointment.doctor.user.username + " at " + str(appointment.date_time))
            return HttpResponseRedirect("/healthnet/patient/appointments/")
        else:
            print(appointment_form.errors)
    else:
        appointment_form = PatientAppointmentForm(instance=ap)
    h = UserProfile.objects.get(user=request.user).hospital
    dp = DoctorProfile.objects.filter(hospital=h)
    appointment_form.fields['doctor'].queryset = dp

    context = {"appointment_form" : appointment_form, 'pk' : pk}
    return render(request, 'patient/patient_edit_appointment.html', context)

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def delete_appointment(request, pk):
    """
    Patient will be able to delete their appointment
    :param request: Accepts a request object
    :return: All appointments for that user
    """
    ap = Appointment.objects.get(id=pk)
    logger.info("Patient \"" + ap.user.username + "\" has deleted his/her apointment "
                "with Doctor " + ap.doctor.user.username + " at " + str(ap.date_time))
    if ap.user == request.user:
        ap.delete()
    return HttpResponseRedirect("/healthnet/patient/appointments/")

@login_required
@user_passes_test(is_patient, login_url='/healthnet/restricted/')
def view_medical_info(request):
    """
    Patient will be able to view and export their information
    :param request: Accepts a request object
    :return: All the medical information
    """
    userProfile = UserProfile.objects.get(user=request.user)
    
    prescriptions = Prescription.objects.filter(user=userProfile.user)
    plen = int(prescriptions.count())

    tests = Test.objects.filter(user=userProfile.user)
    tlen = int(tests.count())

    if request.method == 'POST':
        if 'export' in request.POST:
            import csv
            from django.utils.encoding import smart_str
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = str("attachment; filename=" + 
                userProfile.user.first_name + "_" +
                userProfile.user.last_name + "_Medical_Info.csv")
            writer = csv.writer(response, csv.excel)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"Prescription"),
            ])
            writer.writerow([
                smart_str(u"Doctor Prescribed"),
                smart_str(u"Name of Prescription"),
                smart_str(u"Amount"),
                smart_str(u"Reason"),
                smart_str(u"Time Created"),
            ])
            for obj in Prescription.objects.filter(user=request.user):
                writer.writerow([
                    smart_str(obj.prescribed_by_doctor),
                    smart_str(obj.name),
                    smart_str(obj.amount),
                    smart_str(obj.reason),
                    smart_str(obj.created_at),
                ])
            writer.writerow([
            ])
            writer.writerow([
                smart_str(u"Tests"),
            ])
            writer.writerow([
                smart_str(u"Doctor Prescribed"),
                smart_str(u"Name of Test"),
                smart_str(u"Result"),
                smart_str(u"Reason"),
                smart_str(u"Time Created"),
            ])
            for obj in Test.objects.filter(user=request.user):
                writer.writerow([
                    smart_str(obj.prescribed_by_doctor.user.first_name + " " 
                        + obj.prescribed_by_doctor.user.last_name),
                    smart_str(obj.name_of_test),
                    smart_str(obj.result),
                    smart_str(obj.reason),
                    smart_str(obj.created_at),
                ])
            return response

    userForm = PatientForm(data=model_to_dict(userProfile.user))
    userProfileForm = PatientProfileForm(data=model_to_dict(userProfile))

    userProfileForm.fields['hospital'].widget = forms.HiddenInput()

    context = {"userprofile" : userProfile, "userprofileform" : userProfileForm,
    "pscripts" : prescriptions, "tests" : tests, "plen" : plen, "tlen" : tlen,
    "files" : PatientFile.objects.filter(user=userProfile.user),}
    return render(request, 'patient/patient_view_medical_info.html', context)