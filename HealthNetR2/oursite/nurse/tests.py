from django.test import TestCase
from .forms import *
from healthnet.models import DoctorProfile

class FormsTestCases(TestCase):
    def testNurseForm(self):
        form_data = {'username': 'Georgina',
		     'email' : 'Georgina@gmail.com',
                    'password':'Georgina',
		    'first_name':'Georgina'
                    ,'last_name':'Georgina'}
        form = NurseForm(data = form_data)
        self.assertTrue(form.is_valid())

    def testNurseProfileFormBV1(self):
        form_data = {'user': 0,
		     'previous_employment' : 'Saint E',
                    'hospital':'Hosp'}
        form = NurseProfileForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseProfileFormBV2(self):
        form_data = {'username': 'Georgina',
		     'email' : 'Georgina@gmail.com',
                    'password':'Georgina',
		    'first_name':'Georgina'
                    ,'last_name':'Georgina'}
        nurse = NurseForm(data = form_data)

        form_data = {'user': nurse,
		     'previous_employment' : 'Saint E',
                    'hospital':0}
        form = NurseProfileForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseProfileFormBV3(self):
        form_data = {'username': 'Georgina',
		     'email' : 'Georgina@gmail.com',
                    'password':'Georgina',
		    'first_name':'Georgina'
                    ,'last_name':'Georgina'}
        nurse = NurseForm(data = form_data)

        form_data = {'user': nurse,
		     'previous_employment' : 'Saint E',
                    }
        form = NurseProfileForm(data = form_data)
        self.assertFalse(form.is_valid())


    def testNurseProfileFormBV4(self):
        form_data = {'username': 'Georgina',
		     'email' : 'Georgina@gmail.com',
                    'password':'Georgina',
		    'first_name':'Georgina'
                    ,'last_name':'Georgina'}
        nurse = NurseForm(data = form_data)

        form_data = {}
        form = NurseProfileForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV1(self):
        form_data = {
            'user' : 0,
            'doctor' : DoctorProfile,
            'length' : 20,
            'date_time' : '2015/12/18 12:12:12',
            'reason_for_appointment' : 'pain',
            'additional_information' : 'none'
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV2(self):
        form_data = {
            'user' : User,
            'doctor' : 0,
            'length' : 20,
            'date_time' : '2015/12/18 12:12:12',
            'reason_for_appointment' : 'pain',
            'additional_information' : 'none'
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV3(self):
        form_data = {
            'user' : User,
            'doctor' : DoctorProfile,
            'length' : '0',
            'date_time' : '2015/12/18 12:12:12',
            'reason_for_appointment' : 'pain',
            'additional_information' : 'none'
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV4(self):
        form_data = {
            'user' : User,
            'doctor' : DoctorProfile,
            'length' : 20,
            'date_time' : "12",
            'reason_for_appointment' : 'pain',
            'additional_information' : 'none'
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV5(self):
        form_data = {
            'user' : User,
            'doctor' : DoctorProfile,
            'length' : 20,
            'date_time' : '2015/12/18 12:12:12',
            'reason_for_appointment' : 0,
            'additional_information' : 'none'
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testNurseAppointmentFormBV6(self):
        form_data = {
            'user' : User,
            'doctor' : DoctorProfile,
            'length' : 20,
            'date_time' : '2015/12/18 12:12:12',
            'reason_for_appointment' : 'none',
            'additional_information' : 0
        }
        form = NurseAppointmentForm(data = form_data)
        self.assertFalse(form.is_valid())