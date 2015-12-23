from django import forms
from django.contrib.auth.models import User, Group
from healthnet.models import UserProfile, Appointment, Prescription, Test, Transfer, PatientFile
import datetime
from django.forms import extras
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone

class DoctorMakeAppoitmentForm(forms.Form):
    """
    Doctor form used for the updating the appointment information
    """
    username = forms.CharField(max_length=200)
    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('"%s" is not a patient.' % username)
        return username

    def __init__(self, *args, **kwargs):
        super(DoctorMakeAppoitmentForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

class DoctorUserForm(forms.ModelForm):
    """
    Doctor form used for the updating the doctors user information
    """
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))

    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('"%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

class PrescriptionForm(forms.ModelForm):
    """
    Doctor form used for the updating the Prescription information
    """
    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Prescription
        fields = ('name', 'amount','reason',)

class TestForm(forms.ModelForm):
    """
    Doctor form used for the updating the test information
    """
    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(TestForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Test
        fields = ('name_of_test', 'result','reason',)

class AdmitReleaseForm(forms.ModelForm):
    """
    Doctor form used for the updating the admit/release information
    """
    def __init__(self, *args, **kwargs):
        super(AdmitReleaseForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = UserProfile
        fields = ('is_in_hospital',)

class TransferForm(forms.ModelForm):
    """
    Doctor form used for the updating the transfer information
    """
    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Transfer
        fields = ('reason', 'to_hospital',)

class UploadFileForm(forms.ModelForm):
    """
    Doctor form used for the updating the file information
    """
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = PatientFile
        fields = ('patient_file','file_name',)