from django.test import TestCase
from .forms import *

class FormsTestCases(TestCase):
    def testPatientsForm(self):
        form_data = {'username': 'George','email' : 'George@gmail.com',
                    'password':'George','first_name':'George'
                    ,'last_name':'George'}
        form = PatientForm(data = form_data)
        self.assertTrue(form.is_valid())

    def testPatientsFormBV1(self):
        form_data = {'email' : 'George@gmail.com',
                    'password':'George','first_name':'George'
                    ,'last_name':'George'}
        form = PatientForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPatientsFormBV2(self):
        form_data = {'username': 'George',
                    'password':'George','first_name':'George'
                    ,'last_name':'George'}
        form = PatientForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPatientsFormBV3(self):
        form_data = {'username': 'George','email' : 'George@gmail.com','first_name':'George'
                    ,'last_name':'George'}
        form = PatientForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPatientsFormBV4(self):
        form_data = {'username': 'George','email' : 'George@gmail.com',
                    'password':'George',}
        form = PatientForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPatientForm(self):
        form_data = {'username': 'George','email' : 'George@gmail.com',
                    'password':'George','first_name':'George'
                    ,'last_name':'George'}
        form = PatientForm(data = form_data)
        self.assertTrue(form.is_valid())

    def testPatientProfileForm(self):
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : 'Saint Hospital',
                     'ssn' : 135234,
                     'age' : 20,
                     }
        form = PatientForm(data = form_data)
        self.assertTrue(form.is_valid())

        self.assertFalse(not form.is_valid())
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : "SH",
                     'ssn' : 135234,
                     'age' : -1,
                     }

        self.assertFalse(not form.is_valid())
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : "SH",
                     'ssn' : 135234,
                     'age' : 151,
                     }

    def testPatientEditProfileForm(self):
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : 'Saint Hospital',
                     'ssn' : 135234,
                     'age' : 20,
                     }
        form = PatientForm(data = form_data)
        self.assertFalse(not form.is_valid())
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : 'Saint Hospital',
                     'ssn' : 135234,
                     'age' : -1,
                     }
        self.assertFalse(not form.is_valid())
        form_data = {'username': 'George',
                     'email' : 'George@gmail.com',
                     'password':'George',
                     'first_name':'George',
                     'last_name':'George',
                     'hospital' : 'SH',
                     'ssn' : 135234,
                     'age' : 151,
                     }
        form = PatientForm(data = form_data)
        self.assertTrue(form.is_valid())

