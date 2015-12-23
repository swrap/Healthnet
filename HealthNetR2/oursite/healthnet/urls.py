from django.conf.urls import url

# Url patterns that django follows and directs to the specified views.
urlpatterns = [
    url(r'^$', 'healthnet.views.index', name='index'),
    url(r'^logout/$', 'healthnet.views.user_logout', name='logout'),
    url(r'^login/$', 'healthnet.views.user_login', name='login'),
    url(r'^messages/$', 'healthnet.views.user_messages', name='messages'),
    url(r'^newmessage/$', 'healthnet.views.user_new_message', name='newmessage'),
    url(r'^restricted/$', 'healthnet.views.restricted', name='restricted'),
]