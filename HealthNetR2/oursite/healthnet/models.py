from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator, MaxValueValidator
import datetime
from itertools import chain
import os

from django.core.exceptions import ValidationError
"""
For all of the models we need to have the right format for each of the inputs
and we also need the models to have the right error messages and default values.
Maybe even add some checklists to them.
"""
class Hospital(models.Model):

    name = models.CharField(max_length=100, blank=False, default="")

    def numberAdmittedPatients(self):
        hospital = Hospital.objects.filter(name=self.name)[0]
        patients = UserProfile.objects.filter(hospital=hospital)
        count = int(0)
        for p in patients:
            if(p.is_in_hospital):
                count+=1
        return count

    def patientCount(self):        
        hospital = Hospital.objects.filter(name=self.name)[0]
        patients = UserProfile.objects.filter(hospital=hospital)
        return patients.count()

    def doctorCount(self):
        hospital = Hospital.objects.filter(name=self.name)[0]
        doctors = DoctorProfile.objects.filter(hospital=hospital)
        return doctors.count()

        #not doctors or patients
    def staffCount(self):
        hospital = Hospital.objects.filter(name=self.name)[0]
        staff = StaffProfile.objects.filter(hospital=hospital)
        return staff.count()

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User,null=True)
    previous_employment = models.CharField(max_length=200,blank=False, default="None")
    education_information = models.CharField(max_length=200,blank=False, default="None")
    accreditation = models.CharField(max_length=200,blank=False, default="None")
    licenses = models.CharField(max_length=200,blank=False, default="None")
    hospital = models.ManyToManyField(Hospital)

    def getName(self):
        return str(self.user.username)

    def getAllAppointments(self):
        app_all = Appointment.objects.all()
        app_sel = []
        for e in app_all:
            if e.getDoctor() == self.user.username:
                temp = [e,]
                app_sel = list(chain(app_sel, temp))
        return app_sel
        
    def __str__(self):
        return str(self.user.first_name)

class StaffProfile(models.Model): #nurse or secretary
    user = models.OneToOneField(User,null=True)
    previous_employment = models.CharField(max_length=200,blank=False, default="None")
    education_information = models.CharField(max_length=200,blank=False, default="None")
    accreditation = models.CharField(max_length=200,blank=False, default="None")
    licenses = models.CharField(max_length=200,blank=False, default="None")
    hospital = models.ForeignKey(Hospital,blank=True,default=1)

    def __str__(self):
        return self.user.first_name

class UserProfile(models.Model):
    """
    User Profile model that accesses Django's authorization model for the User class.
    Extra fields are added to this user profile model.
    """

    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )

    user = models.OneToOneField(User,null=True)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(150)],default=0)
    date_of_birth = models.DateField(blank=False, default=datetime.datetime.now)
    spouse_first_name = models.CharField(max_length=200, blank=False,default="None")
    next_of_kin = models.CharField(max_length=200, blank=False, default="None") 
    emergency_contact = models.CharField(max_length=200, blank=False, default="None")
    ssn = models.SmallIntegerField(blank=False, default=135234)
    numb = RegexValidator(regex=r'^\+?1?\d{9,15}$', message = ("Format +999999999."))
    phone_number = models.CharField(max_length=15, validators=[numb], blank=False, default="+999999999")
    sex = models.CharField(max_length=200,choices=SEX_CHOICES, default="")
    weight = models.IntegerField(blank=True, null=True, default=0)
    height = models.IntegerField(blank=True, null=True, default=0)
    insurance = models.CharField(max_length=200,blank=False, default="None")
    prescription = models.CharField(max_length=200, blank=False, default="None")
    hospital = models.ForeignKey(Hospital,blank=True,default=1)
    is_in_hospital = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    """
    Appointment model that is composed of appointment fields.
    """
    user = models.ForeignKey(User,null=True)
    length = models.IntegerField(blank=True, null=True, default=30)
    date_time = models.DateTimeField(default=datetime.datetime.now,help_text="YYYY/MM/DD HH:MM:SS")
    reason_for_appointment = models.CharField(max_length=200, blank=False, default="None")
    additional_information = models.CharField(max_length=200, blank=False, default="None")
    doctor = models.ForeignKey(DoctorProfile,null=True)

    def __str__(self):        
        return self.user.username

class Message(models.Model):
    from_user = models.CharField(max_length=200, default="None")
    to_user = models.CharField(max_length=200, default="None")
    date_time = models.DateTimeField(default=datetime.datetime.now)
    message = models.CharField(max_length=500, default="None")

class Prescription(models.Model):
    user = models.ForeignKey(User,null=True)
    prescribed_by_doctor = models.ForeignKey(DoctorProfile,null=True)
    name = models.CharField(max_length=200,blank=False, default="None")
    amount = models.CharField(max_length=200,blank=False, default="None")
    reason = models.CharField(max_length=200,blank=False, default="None")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class Test(models.Model):
    user = models.ForeignKey(User,null=True)
    prescribed_by_doctor = models.ForeignKey(DoctorProfile,null=True)
    name_of_test = models.CharField(max_length=200,blank=False, default="None")
    result = models.CharField(max_length=200,blank=False, default="None")
    reason = models.CharField(max_length=200,blank=False, default="None")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class Transfer(models.Model):
    user = models.ForeignKey(User,null=True)
    reason = models.CharField(max_length=200,blank=False, default="None")
    from_hospital = models.CharField(max_length=200,blank=False, default="None")
    to_hospital = models.ForeignKey(Hospital,blank=True,default=1)

class PatientFile(models.Model):
    user = models.ForeignKey(User,null=True)
    file_name = models.CharField(max_length=200,blank=False, default="None")
    patient_file = models.FileField(upload_to='patient/fileuploads/')

    def extension(self):
        file_name, extension = os.path.splitext(self.patient_file.name)
        return extension.lower()