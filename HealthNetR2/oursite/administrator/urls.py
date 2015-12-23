from django.conf.urls import url

# Url patterns that django follows and directs to the specified views.
urlpatterns = [
    url(r'^$', 'administrator.views.index', name='index'),
    url(r'^createuser/$', 'administrator.views.create_user', name='newuser'),
    url(r'^edituser/$', 'administrator.views.edit_user', name='edituser'),
    url(r'^messages/$', 'healthnet.views.user_messages', name='messages'),
    url(r'^transfer/(?P<pk>[-\w]+)/$', 'administrator.views.transfer', name='transfer'),
    url(r'^log/$', 'administrator.views.log', name='log'),
    url(r'^info/$', 'administrator.views.display_info', name='info'),
]