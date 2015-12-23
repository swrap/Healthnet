from django.test import TestCase
from .models import Hospital, Message
from patient.forms import PatientForm

class MessageTestCase(TestCase):
    def setUp(self):
        Message.objects.create(from_user = "George",
        to_user = "Bob",
        message = "hello world")

    def testMessageSetUp(self):
        mes = Message.objects.get(to_user="Bob")
        self.assertEqual(mes.to_user,"Bob")
        self.assertEqual(mes.from_user,"George")
        self.assertEqual(mes.message, "hello world")


class HospitalTestCase(TestCase):
    def setUp(self):
        Hospital.objects.create(name="Hospital")#, admitted_patient_count = 300,
       # patient_count = 500, doctor_count = 20, staff_count = 50)

        Hospital.objects.create(name="Mayo")#, admitted_patient_count = 100,
       # patient_count = 200, doctor_count = 10, staff_count = 30)

    def test_hospital_set_up(self):
        Hosp = Hospital.objects.get(name="Hospital")
        Mayo = Hospital.objects.get(name="Mayo")
        self.assertEqual(Hosp.name,"Hospital")
        self.assertEqual(Mayo.name,"Mayo")


