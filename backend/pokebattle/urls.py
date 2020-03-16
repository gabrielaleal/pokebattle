from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views

from users.views import SignUpView, UserLoginView, UserLogoutView


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^jsreverse/$", django_js_reverse.views.urls_js, name="js_reverse"),
    url(r"^$", TemplateView.as_view(template_name="home.html"), name="home"),
    url(r"^battles/", include("battles.urls"), name="battles"),  # import all urls from battles app
    url(r"^signup/", SignUpView.as_view(), name="signup"),
    url(r"^login/", UserLoginView.as_view(), name="login"),
    url(r"^logout/", UserLogoutView.as_view(), name="logout"),
]
