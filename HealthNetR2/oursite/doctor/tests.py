from django.test import TestCase
from healthnet.models import *
from .forms import *

class FormsTestCases(TestCase):
    def testPrescriptionForm(self):
        form_data = {'name' : 'drug',
                    'amount' : 20,
                    'reason' : 'need it'}
        form = PrescriptionForm(data = form_data)
        self.assertTrue(form.is_valid())

    def testPrescriptionFormBV1(self):
        form_data = {
                    'amount' : 20,
                    'reason' : 'need it'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPrescriptionFormBV2(self):
        form_data = {'name' : 'drug',
                    'reason' : 'need it'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testPrescriptionFormBV3(self):
        form_data = {'name' : 'drug',
                    'amount' : '20'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testTestForm(self):
        form_data = {'name_of_test' : 'drug',
                    'result' : 'negative',
                    'reason' : 'blood test'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testTestFormBV1(self):
        form_data = {
                    'result' : 'negative',
                    'reason' : 'blood test'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testTestFormBV2(self):
        form_data = {'name_of_test' : 'drug',
                    'reason' : 'blood test'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testTestFormBV3(self):
        form_data = {'name_of_test' : 'drug',
                    'result' : 'negative'}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())

    def testTestFormBV4(self):
        form_data = {}
        form = PrescriptionForm(data = form_data)
        self.assertFalse(form.is_valid())