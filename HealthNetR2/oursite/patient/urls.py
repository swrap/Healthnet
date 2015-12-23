from django.conf.urls import url
import healthnet
# Url patterns that django follows and directs to the specified views.
urlpatterns = [
    url(r'^$', 'patient.views.index', name='patient_index'),
    url(r'^register/$', 'patient.views.register', name='register'),
    url(r'^editpatient/$', 'patient.views.edit_patient', name='editpatient'),
    url(r'^appointments/$', 'patient.views.appointments', name='viewappoinments'),
    url(r'^makeappointment/$', 'patient.views.make_appointment', name='makeappointment'),
    url(r'^editappointment/(?P<pk>[-\w]+)/$', 'patient.views.edit_appointment', name='editapp'),
    url(r'^deleteappointment/(?P<pk>[-\w]+)/$', 'patient.views.delete_appointment', name='deleteapp'),
    url(r'^messages/$', 'healthnet.views.user_messages', name='messages'),
    url(r'^viewmedicalinfo/$', 'patient.views.view_medical_info', name='viewmedicalinfo'),
]