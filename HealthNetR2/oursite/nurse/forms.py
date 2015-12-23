from django import forms
from healthnet.models import Appointment, StaffProfile
from django.contrib.auth.models import User, Group
import datetime


class NurseForm(forms.ModelForm):
    """
    Nurse form used for the updating the nurse user information
    """
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    # checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('"%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs):
        super(NurseForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class NurseProfileForm(forms.ModelForm):
    """
    Nurse form used for the updating the nurse profile information
    """
    def __init__(self, *args, **kwargs):
        super(NurseProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = StaffProfile
        fields = ('previous_employment','education_information','accreditation', 'licenses', 'hospital')

class NurseAppointmentForm(forms.ModelForm):
    """
    Nurse form used for the updating the patient appointment information
    """
    def __init__(self, *args, **kwargs):
        super(NurseAppointmentForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    def clean_length(self):
        length = self.cleaned_data['length']
        if length < 15:
            raise forms.ValidationError("Minimum is 15 minutes")
        return length

    def clean_date_time(self):
        #changed from data, might pose issues
        length = self.data['length']
        dt = self.cleaned_data['date_time']

        #check if appointment is 24 hours before
        today = datetime.date.today()
        tempD = dt.date()
        if tempD.year < today.year:
            raise forms.ValidationError("Appointments must be made 24hrs before.")
            return dt
        if tempD.month < today.month:
            raise forms.ValidationError("Appointments must be made 24hrs before.")
            return dt
        if tempD.day < today.day:
            raise forms.ValidationError("Appointments must be made 24hrs before.")
            return dt
        if (dt - datetime.timedelta(hours=int(24))) < datetime.datetime.now():
            raise forms.ValidationError("Appointments must be made 24hrs before.")
            return dt

        if dt.hour < 9:
            raise forms.ValidationError("Doctor hours open at 9AM.")
            return dt
        if dt.hour >= 17:
            raise forms.ValidationError("Doctor hours close at 5PM.")
            return dt

        #check for overlapping appointments
        if int(length) > 15:
            #gets doctor
            doctor = self.cleaned_data['doctor']
            #cleans out doctor appointments and cleans out itself itself
            all_app = Appointment.objects.filter(doctor=doctor).exclude(pk=self.instance.pk)

            for app in all_app:
                #if the appointments are on the same day
                if app.date_time.date() == dt.date():
                    a = app.date_time
                    a_start = a.strftime("%H:%M")
                    a_end = (a + datetime.timedelta(minutes=int(app.length))).strftime("%H:%M")
                    dt_start = dt.strftime("%H:%M")
                    dt_end = (dt + datetime.timedelta(minutes=int(length))).strftime("%H:%M")
                    #if starts before and ends after dt_time
                    if a_start < dt_start and a_end > dt_start:
                        raise forms.ValidationError("Conflict (Start time of another appointment): %s" % (dt_start))
                        return dt
                    #if it starts after but the other appointment ends after
                    elif a_start > dt_start and dt_end > a_start:
                        raise forms.ValidationError("Conflict (End time of another appointment): %s" % (dt_end))
                        return dt
        return dt

    class Meta:
        model = Appointment
        fields = ('user','doctor','length', 'date_time',
                  'reason_for_appointment', 'additional_information')