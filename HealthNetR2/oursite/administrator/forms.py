from django import forms
from django.contrib.auth.models import User, Group
from healthnet.models import *

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(AdminForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

class AdminEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(AdminEditForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('username', 'email','password','first_name','last_name')

class DoctorForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(DoctorForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

class DoctorProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(DoctorProfileForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = DoctorProfile
        fields = ('previous_employment','education_information','accreditation',
            'licenses','hospital',)

class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    group = forms.ModelChoiceField(queryset=Group.objects.exclude(name="Doctor").exclude(name="Patient"), empty_label="Choose Below")

    #checks to see if the username is in existance already
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(StaffForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

class StaffProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(StaffProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = StaffProfile
        fields = ('previous_employment','education_information','accreditation',
            'licenses','hospital',)