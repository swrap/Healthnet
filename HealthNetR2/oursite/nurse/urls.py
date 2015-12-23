from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'nurse.views.index', name='index'),
    url(r'^search/', 'nurse.views.search_patient', name='patientsearch'),
    url(r'^patientsearch/', 'nurse.views.search_patient', name='patientfound'),
    url(r'^makeappointment/(?P<pk>[-\w]+)/', 'nurse.views.make_appointment', name='makeappointment'),
    url(r'^editprofile/', 'nurse.views.edit_Profile', name='editprofile'),
    url(r'^editappointment/(?P<pk>[-\w]+)/$', 'nurse.views.edit_appointment', name='editapp'),
    url(r'^deleteappointment/(?P<pk>[-\w]+)/$', 'nurse.views.delete_appointment', name='deleteapp'),
    url(r'^viewpatientappointment/(?P<pk>[-\w]+)/$', 'nurse.views.appointments', name='viewpatientapps'),
    url(r'^allpatients/$', 'nurse.views.all_patients', name='allpatients'),
    url(r'^viewpatient/(?P<pk>[-\w]+)/$', 'nurse.views.view_patient', name='viewpatient'),
]
