from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from doctor.templatetags.doctor_tags import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from healthnet.models import DoctorProfile, Appointment, Prescription, Test, Hospital
from doctor.forms import *
from patient.forms import PatientAppointmentForm, PatientProfileForm, PatientForm
from doctor.templatetags.doctor_tags import *
from django.forms.models import model_to_dict
from administrator.forms import DoctorProfileForm
from django import forms

import logging;
import json as simplejson
import json
from django.utils.safestring import SafeString

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def index(request):
    """
    Doctor index page is loaded
    :param request: Accepts a request object.
    :return: The index page for the doctor
    """
    appointmentdic = []
    appointments = Appointment.objects.filter(doctor=DoctorProfile.objects.get(user=request.user))
    for appointment in appointments:
        d = appointment.date_time
        starttime = d.strftime("%Y-%m-%dT%H:%M:%S")
        appointmentdic.append({'title': appointment.user.first_name,
                               'start': starttime
                               })
    context = {"allAppointments": SafeString(simplejson.dumps(appointmentdic))}
    return render(request, 'doctor/doctor_index.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def all_patients(request):
    """
    Doctor view for all of the patients in the system
    :param request: Accepts a request object.
    :return: The list of patients in html page
    """
    if request.method == 'GET':
        if 'patientname' in request.GET:
            patient = request.GET.get('patientname')
            user = User.objects.filter(username=patient)
            if user.exists() and user[0].groups.filter(name="Patient"):
                userProfile = UserProfile.objects.filter(user=user)[0]
                pkofuser = userProfile.id
                return view_patient(request,pkofuser)
        if 'home' in request.GET:
            return HttpResponseRedirect("/healthnet/doctor/")

        allP = UserProfile.objects.all()
        length = int(allP.count())
    context = {"allp" : allP, "len" : length}
    return render(request, 'doctor/doctor_view_all_patients.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def view_patient(request,pk):
    """
    Doctor view for a specific patient in the system
    :param request: Accepts a request object.
    :param pk: Private Key for a user
    :return: The view in html format for a specific patient
    """
    userProfile = UserProfile.objects.get(id=pk)
    
    prescriptions = Prescription.objects.filter(user=userProfile.user)
    plen = int(prescriptions.count())

    tests = Test.objects.filter(user=userProfile.user)
    tlen = int(tests.count())

    if request.method == 'GET':
        if 'makepscript' in request.GET:
            return HttpResponseRedirect('/healthnet/doctor/makeprescription/%s/' % userProfile.id)
        elif 'maketest' in request.GET:
            return HttpResponseRedirect('/healthnet/doctor/maketest/%s/' % userProfile.id)
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
        elif 'uploadfile' in request.GET:
            return upload_file(request, userProfile.id)

    userForm = PatientForm(data=model_to_dict(userProfile.user))
    userProfileForm = PatientProfileForm(data=model_to_dict(userProfile))

    userProfileForm.fields['hospital'].widget = forms.HiddenInput()

    dp = DoctorProfile.objects.get(user=request.user)
    dph = dp.hospital.filter(name=userProfile.hospital.name)
    if dph.exists() and dp.hospital.count() < 2: 
        temp = False
    else:
        temp = True

    context = {"userprofile" : userProfile, "userprofileform" : userProfileForm,
    "pscripts" : prescriptions, "tests" : tests, "plen" : plen, "tlen" : tlen,
    "cantransfer" : temp,
    "files" : PatientFile.objects.filter(user=userProfile.user),}
    return render(request, 'doctor/doctor_view_patient.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def appointments(request):
    """
    Doctor view of all of the appointments for the specific doctor
    :param request: Accepts a request object.
    :return: The view in html format for the appointments for the doctor
    """
    doc = DoctorProfile.objects.filter(user=request.user)[0]
    allAppointments = Appointment.objects.filter(doctor=doc)
    length = int(allAppointments.count())

    if request.method == 'POST':
        if 'home' in request.POST:
            return HttpResponseRedirect("/healthnet/doctor/")
        elif 'delete_all' in request.POST:
            allAppointments = allAppointments.delete()
            length = 0
        elif 'make' in request.POST:
            return HttpResponseRedirect("/healthnet/doctor/makeappointment/")

    context = {"all_appointments" : allAppointments, "len" : length}
    return render(request, 'doctor/doctor_appointment.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def make_appointment(request):
    """
    Doctor view for making a specific appointment for a specific patient
    :param request: Accepts a request object.
    :return: The view in html format for making an appointment for a user
    """
    if request.method == 'POST':
        doc_make_form = DoctorMakeAppoitmentForm(data=request.POST)

        #sets the doctor to the current Doctor
        request_copy = request.POST.copy()
        request_copy.update(doctor=DoctorProfile.objects.get(user=request.user).id)
        appointment_form = PatientAppointmentForm(data=request_copy)

        if doc_make_form.is_valid() and appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.user = User.objects.get(username=doc_make_form.cleaned_data['username'])
            appointment.doctor = DoctorProfile.objects.get(user=request.user)
            appointment.save()

            logger.info("Doctor \"" + request.user.username + "\" has added an apointment "
                "for Patient \"" + appointment.user.username + "\" at " + str(appointment.date_time))
            return HttpResponseRedirect("/healthnet/doctor/appointments/")
        else:
            print(appointment_form.errors)
    else:
        doc_make_form = DoctorMakeAppoitmentForm()
        appointment_form = PatientAppointmentForm()
    
    appointment_form.fields['doctor'].widget = forms.HiddenInput()

    appointmentdic = []
    appointments = Appointment.objects.all()
    for appointment in appointments:
        d = appointment.date_time
        starttime = d.strftime("%Y-%m-%dT%H:%M:%S")
        appointmentdic.append({'title': appointment.user.first_name,
                               'start': starttime
                               })

    context = {"allAppointments": SafeString(simplejson.dumps(appointmentdic)),
    "doc_make_form" : doc_make_form, "appointment_form" : appointment_form,}
    return render(request, 'doctor/doctor_make_appointment.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def make_prescription(request,pk):
    """
    Doctor view for making a specific appointment for a specific patient
    :param request: Accepts a request object.
    :param pk: Private Key for a user
    :return: The view in html format for making an appointment for a user
    """
    if request.method == 'POST':
        pscript_form = PrescriptionForm(data=request.POST)

        if pscript_form.is_valid():
            script = pscript_form.save(commit=False)
            script.user = UserProfile.objects.get(id=pk).user
            u = User.objects.get(id=request.user.id)
            script.prescribed_by_doctor = DoctorProfile.objects.get(user=u)
            script.save()

            logger.info("Doctor \"" + request.user.username + "\" has added a prescription "
                "for Patient " + script.user.username + "." )
            return view_patient(request,pk)
        else:
            print(pscript_form.errors)
    else:
        pscript_form = PrescriptionForm()

    context = {"form" : pscript_form, "pk" : pk}
    return render(request, 'doctor/doctor_make_prescription.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def make_test(request,pk):
    """
    Doctor view for making a specific appointment for making a test
    :param request: Accepts a request object.
    :param pk: Private Key for a user
    :return: The view in html format for making an appointment for a user
    """
    if request.method == 'POST':
        test_form = TestForm(data=request.POST)

        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.user = UserProfile.objects.get(id=pk).user
            u = User.objects.get(id=request.user.id)
            test.prescribed_by_doctor = DoctorProfile.objects.get(user=u)
            test.save()

            logger.info("Doctor \"" + request.user.username + "\" has added a test "
                "for Patient \"" + test.user.username + "\"." )
            return view_patient(request,pk)
        else:
            print(appointment_form.errors)
    else:
        pscript_form = TestForm()

    context = {"form" : TestForm, "pk" : pk}
    return render(request, 'doctor/doctor_make_test.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def edit_profile(request):
    """
    Doctor view for editing the doctors profile
    :param request: Accepts a request object.
    :return: The view for editing their profile django
    """
    d = DoctorProfile.objects.get(user=request.user)
    doctor_form = DoctorProfileForm(instance=d)

    if request.method == 'POST':
        doctor_form = DoctorProfileForm(data=request.POST,instance=d)
        if doctor_form.is_valid():
            doctor = doctor_form.save(commit=False)
            doctor.hospital = doctor_form.cleaned_data['hospital']
            doctor.save()
            logger.info("Doctor \"" + request.user.username + "\" has edited their profile.")
            return HttpResponseRedirect("/healthnet/doctor/editprofile/")
        else:
            print(doctor_form.errors)

    context = {"doctor_form" : doctor_form}
    return render(request, 'doctor/doctor_edit_profile.html', context)


@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def edit_appointment(request, pk):
    """
    Doctor view for editing the doctors profile
    :param request: Accepts a request object.
    :param pk: Private Key for a user
    :return: The view for editing their profile in html format
    """
    ap = Appointment.objects.get(id=pk)
    appointment_form = PatientAppointmentForm(instance=ap)

    if request.method == 'POST':
        appointment_form = PatientAppointmentForm(data=request.POST,instance=ap)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.save()
            appointment_form.save()
            logger.info("Doctor \"" + request.user.username + "\" has edited an apointment "
                "for Patient \"" + appointment.user.username + "\" at " + str(appointment.date_time))
            return HttpResponseRedirect("/healthnet/doctor/appointments/")
        else:
            print(appointment_form.errors)

    appointment_form.fields['doctor'].widget = forms.HiddenInput()

    context = {"appointment_form" : appointment_form, 'pk' : pk}
    return render(request, 'doctor/doctor_edit_appointment.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def edit_test(request, pk, pk2):
    """
    Doctor view for editing the patients tests
    :param request: Accepts a request object.
    :param pk: Private Key for the appointments
    :param pk2: Private Key for a user
    :return: The view for editing the patients test in html format
    """
    t = Test.objects.get(id=pk)
    test_form = TestForm(instance=t)

    if request.method == 'POST':
        test_form = TestForm(data=request.POST,instance=t)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.save()

            logger.info("Doctor \"" + request.user.username + "\" has edited the test "
                "for Patient \"" + test.user.username + "\".")
            return view_patient(request,pk2)
        else:
            print(test_form.errors)

    context = {"test_form" : test_form, 'pk' : pk, "pk2" : pk2}
    return render(request, 'doctor/doctor_edit_test.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def delete_appointment(request, pk):
    """
    Doctor view for deleting the patients appointments
    :param request: Accepts a request object.
    :return: The view for deleting patients appointments
    """
    ap = Appointment.objects.get(id=pk)
    logger.info("Doctor \"" + request.user.username + "\" has deleted his/her apointment "
                "with Patient \"" + ap.user.username + "\" at " + str(ap.date_time))
    if ap.doctor.user.username == request.user.username:
        ap.delete()
    return HttpResponseRedirect("/healthnet/doctor/appointments/")

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def delete_prescription(request, pk, pk2):
    """
    Doctor view for deleting the patients prescrition
    :param request: Accepts a request object.
    :param pk: Private Key for the prescrition
    :param pk2: Private Key for a user
    :return: The view for deleting patients prescrition in html format
    """
    p = Prescription.objects.get(id=pk)
    logger.info("Doctor \"" + request.user.username + "\" has deleted his/her prescrition "
                "for Patient \"" + p.user.username + "\". Name of Prescription is " + p.name)
    p.delete()
    return view_patient(request,pk2)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def delete_test(request, pk, pk2):
    """
    Doctor view for deleting the patients tests
    :param request: Accepts a request object.
    :param pk: Private Key for the test
    :param pk2: Private Key for a user
    :return: The view for deleting patients tests in html format
    """
    t = Test.objects.get(id=pk)
    logger.info("Doctor \"" + request.user.username + "\" has deleted his/her test "
                "for Patient \"" + t.user.username + "\". Name of Test is " + t.name_of_test)
    t.delete()
    return view_patient(request,pk2)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def delete_file(request, pk, pk2):
    """
    Doctor view for deleting the patients file
    :param request: Accepts a request object.
    :param pk: Private Key for the file
    :param pk2: Private Key for a user
    :return: The view for deleting patients file in html format
    """
    patientFile = PatientFile.objects.get(id=pk)
    logger.info("Doctor \"" + request.user.username + "\" has deleted "
                " Patient \"" + patientFile.user.username + "\" file named " + 
                patientFile.patient_file.name)
    patientFile.patient_file.delete()
    patientFile.delete()
    return view_patient(request,pk2)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def admit_release_patient(request, pk):
    """
    Doctor view for admitting releasing patients from the hospital
    :param request: Accepts a request object.
    :param pk: Private Key for the user
    :return: The view for admitting/releasing patients from the hospital in html format
    """
    userProfile = UserProfile.objects.get(id=pk)

    if userProfile.is_in_hospital:
        userProfile.is_in_hospital = False
        userProfile.save()
        logger.info("Doctor \"" + request.user.username + "\" has released "
            " Patient \"" + userProfile.user.username + " into " + userProfile.hospital.name + ".")
    else:
        userProfile.is_in_hospital = True
        userProfile.save()
        logger.info("Doctor \"" + request.user.username + "\" has admitted "
            " Patient \"" + userProfile.user.username + "\" out of " + userProfile.hospital.name + ".")

    return HttpResponseRedirect("/healthnet/doctor/viewpatient/%s/" % userProfile.id)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def transfer_patient(request,pk):
    """
    Doctor view for transfering patients from the hospital
    :param request: Accepts a request object.
    :param pk: Private Key for the user
    :return: The view for transfering patients from the hospital in html format
    """
    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST)

        if transfer_form.is_valid():
            transfer = transfer_form.save(commit=False)
            transfer.from_hospital = UserProfile.objects.get(id=pk).hospital.name
            transfer.user = UserProfile.objects.get(id=pk).user
            transfer.save()

            userP = UserProfile.objects.get(id=pk)
            userP.hospital = transfer.to_hospital
            userP.save()

            logger.info("Doctor \"" + request.user.username + "\" has transfered "
                " Patient \"" + transfer.user.username + "\" from Hospital : \"" +  transfer.from_hospital 
                + "\" to Hospital \"" + transfer.to_hospital.name + "\"")
            return HttpResponseRedirect("/healthnet/doctor/viewpatient/%s/" % pk)
        else:
            print(transfer_form.errors)
    else:
        transfer_form = TransferForm()
    dph = DoctorProfile.objects.get(user=request.user).hospital
    transfer_form.fields['to_hospital'].queryset = dph.exclude(id=UserProfile.objects.get(id=pk).hospital.pk)

    context = {"form" : transfer_form, "pk" : pk, "patient" : UserProfile.objects.get(id=pk)}
    return render(request, 'doctor/doctor_transfer_patient.html', context)

@login_required
@user_passes_test(is_doctor, login_url='/healthnet/restricted/')
def upload_file(request,pk):
    """
    Doctor view for uploading a file to the db
    :param request: Accepts a request object.
    :param pk: Private Key for the user
    :return: The view for uploading a file to the db in html format
    """
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            form = file_form.save(commit=False)
            form.user = UserProfile.objects.get(id=pk).user
            form.save()
            logger.info("Doctor \"" + request.user.username + "\" has uploaded a file for "
                " Patient \"" + form.user.username + "\".")
            return HttpResponseRedirect("/healthnet/doctor/viewpatient/%s/" % pk)
    else:
        file_form = UploadFileForm()

    context = {"form" : file_form, "patient" : UserProfile.objects.get(id=pk),}
    return render(request, 'doctor/doctor_upload_file.html', context)