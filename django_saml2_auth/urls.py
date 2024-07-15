from django.urls import path, re_path
from . import views

app_name = 'django_saml2_auth'

urlpatterns = [
    path("<uuid:metadata_id>/acs/", views.acs, name="acs"),
    path("otp_login/", views.otp_login, name="otp_login"),
    re_path(r'^welcome/$', views.welcome, name="welcome"),
    re_path(r'^denied/$', views.denied, name="denied"),
]
