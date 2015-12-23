from django.test import TestCase
from .forms import *

class FormsTestCases(TestCase):
    def testAdminForm(self):
            form_data = {'username': 'admin','email' : 'admin@gmail.com',
                        'password':'admin','first_name':'ad'
                        ,'last_name':'min'}
            form = AdminForm(data = form_data)
            self.assertTrue(form.is_valid())

    def testAdminFormBV1(self):
            form_data = {'email' : 'admin@gmail.com',
                        'first_name':'ad'
                        ,'last_name':'min'}
            form = AdminForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminFormBV2(self):
            form_data = {'email' : 'admin@gmail.com',
                        'password':'admin'
                        ,'last_name':'min'}
            form = AdminForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminFormBV3(self):
            form_data = {'email' : 'admin@gmail.com',
                        'password':'admin','first_name':'ad'
                        }
            form = AdminForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminFormBV4(self):
            form_data = {}
            form = AdminForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminFormBV5(self):
            form_data = {}
            form = AdminForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminEditForm(self):
            form_data = {'username': 'admin','email' : 'admin@gmail.com',
                        'password':'admin','first_name':'ad'
                        ,'last_name':'min'}
            form = AdminEditForm(data = form_data)
            self.assertTrue(form.is_valid())
    def testAdminEditFormBV1(self):
            form_data = {'email' : 'admin@gmail.com',
                        'first_name':'ad'
                        ,'last_name':'min'}
            form = AdminEditForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminEditFormBV2(self):
            form_data = {'email' : 0,
                        'password':0
                        ,'last_name':0}
            form = AdminEditForm(data = form_data)
            self.assertFalse(form.is_valid())

    def testAdminEditFormBV3(self):
            form_data = {}
            form = AdminEditForm(data = form_data)
            self.assertFalse(form.is_valid())
