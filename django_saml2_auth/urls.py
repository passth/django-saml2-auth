from django.urls import path, re_path
from . import views

app_name = 'django_saml2_auth'

urlpatterns = [
    path("<uuid:metadata_id>/acs/", views.acs, name="acs"),
    re_path(r'^welcome/$', views.welcome, name="welcome"),
    re_path(r'^denied/$', views.denied, name="denied"),
]
