from django.conf.urls import url

# Url patterns that django follows and directs to the specified views.
urlpatterns = [
    url(r'^$', 'doctor.views.index', name='index'),
    url(r'^editprofile/$', 'doctor.views.edit_profile', name='editprofile'),
    url(r'^appointments/$', 'doctor.views.appointments', name='allappointments'),
    url(r'^makeappointment/$', 'doctor.views.make_appointment', name='makeappointment'),
    url(r'^editappointment/(?P<pk>[-\w]+)/$', 'doctor.views.edit_appointment', name='editapp'),
    url(r'^deleteappointment/(?P<pk>[-\w]+)/$', 'doctor.views.delete_appointment', name='deleteapp'),
    url(r'^messages/$', 'healthnet.views.user_messages', name='messages'),
    url(r'^allpatients/$', 'doctor.views.all_patients', name='allpatients'),
    url(r'^viewpatient/(?P<pk>[-\w]+)/$', 'doctor.views.view_patient', name='viewpatient'),
    url(r'^makeprescription/(?P<pk>[-\w]+)/$', 'doctor.views.make_prescription', name='makepscript'),
    url(r'^deleteprescription/(?P<pk>[-\w]+)/(?P<pk2>[-\w]+)/$', 'doctor.views.delete_prescription', name='deletepscript'),
    url(r'^maketest/(?P<pk>[-\w]+)/$', 'doctor.views.make_test', name='maketest'),
    url(r'^edittest/(?P<pk>[-\w]+)/(?P<pk2>[-\w]+)/$', 'doctor.views.edit_test', name='edittest'),
    url(r'^deletetest/(?P<pk>[-\w]+)/(?P<pk2>[-\w]+)/$', 'doctor.views.delete_test', name='deletetest'),
    url(r'^transferpatient/(?P<pk>[-\w]+)/$', 'doctor.views.transfer_patient', name='transferpatient'),
    url(r'^uploadfile/(?P<pk>[-\w]+)/$', 'doctor.views.upload_file', name='uploadfile'),
    url(r'^deletefile/(?P<pk>[-\w]+)/(?P<pk2>[-\w]+)/$', 'doctor.views.delete_file', name='deletefile'),
]	