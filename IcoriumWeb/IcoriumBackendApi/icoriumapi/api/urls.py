from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^current-icos/$', views.current_ico_list),
    url(r'^upcoming-icos/$', views.upcoming_ico_list),
    url(r'^past-icos/$', views.past_ico_list),
    url(r'^icos-count/$', views.ico_count),
    url(r'^ico/$', views.ico_details),
    url(r'^company/$', views.company),
    url(r'^contact-email/$', views.send_contact_email),
]