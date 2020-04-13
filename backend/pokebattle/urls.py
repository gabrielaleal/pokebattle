from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views

from pokemon.views import PokemonAutocompleteView
from users.views import InviteUserView, SignUpView, UserLoginView, UserLogoutView


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^jsreverse/$", django_js_reverse.views.urls_js, name="js_reverse"),
    url(r"^$", TemplateView.as_view(template_name="home.html"), name="home"),
    url(r"^invite-user/$", InviteUserView.as_view(), name="invite-user"),
    # apps' urls
    url(r"^battles/", include("battles.urls"), name="battles"),
    url(r"^api/", include("api.battles.urls"), name="api"),
    # authentication urls
    url(r"^signup/$", SignUpView.as_view(), name="signup"),
    url(r"^login/$", UserLoginView.as_view(), name="login"),
    url(r"^logout/$", UserLogoutView.as_view(), name="logout"),
    url(r"^oauth/", include("social_django.urls"), name="social"),
    # autocomplete urls
    url(r"^pokemon-autocomplete/$", PokemonAutocompleteView.as_view(), name="pokemon-autocomplete"),
]
