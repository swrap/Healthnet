from django import forms
from django.contrib.auth.models import User, Group
from healthnet.models import UserProfile, DoctorProfile, StaffProfile
from healthnet.models import Message

class MessageForm(forms.ModelForm):
    """
    Message form used for messaging other users
    """
    #checks to see if the username is in existance already
    def clean_to_user(self):
        to = self.cleaned_data['to_user']
        user = self.cleaned_data['from_user']
        if to == user:  
            raise forms.ValidationError('You cannot send a message to yourself.')
            return to
        elif not User.objects.filter(username=to).exists():
            raise forms.ValidationError('"%s" does not exist. Send to valid user.' % to)
            return to
        
        to_user = User.objects.get(username=to)
        from_user = User.objects.get(username=user)
        to_group = to_user.groups.all()[0]
        from_group = from_user.groups.all()[0]

        #patient blocking to only their hospital and to the nurses and doctors
        #of that hospitalx
        if from_group.name == "Patient" and from_group.name == to_group:
            raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Patient" and to_group.name == "Doctor" and not DoctorProfile.objects.get(user=to_user).hospital.all().filter(name=UserProfile.objects.get(user=from_user).hospital).exists():
            raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Patient" and to_group.name == "Nurse" and UserProfile.objects.get(user=from_user).hospital != StaffProfile.objects.get(user=to_user).hospital:
            raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Patient" and to_group.name == "Administrator":
            raise forms.ValidationError("You are not allowed to message this user.")

        #doctor blocking to only their patients of their hospital
        if from_group.name == "Doctor" and to_group.name == "Patient":
            docHospitals = DoctorProfile.objects.get(user=from_user).hospital.all()
            if not docHospitals.filter(name=UserProfile.objects.get(user=to_user).hospital.name).exists():
                raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Doctor" and to_group.name == "Administrator":
            raise forms.ValidationError("You are not allowed to message this user.")

        #nurse blocking to only their patients of their hospital
        if from_group.name == "Nurse" and to_group.name == "Patient" and StaffProfile.objects.get(user=from_user).hospital != UserProfile.objects.get(user=to_user).hospital:
            raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Nurse" and to_group.name == "Administrator":
            raise forms.ValidationError("You are not allowed to message this user.")

        #admin blocking only other admins of their hospital
        if from_group.name == "Administrator" and to_group.name == "Administrator" and StaffProfile.objects.get(user=from_user).hospital != StaffProfile.objects.get(user=to_user).hospital:
            raise forms.ValidationError("You are not allowed to message this user.")
        elif from_group.name == "Administrator" and to_group.name != "Administrator":
            raise forms.ValidationError("You are not allowed to message this user.")

        return to

    def __init__(self, *args, **kwargs): #change code to understand how this lets in marked up fields
        super(MessageForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
        self.fields['from_user'].widget.attrs['readonly'] = True

    class Meta:
        model = Message
        fields = ('from_user','to_user','date_time','message')