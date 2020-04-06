from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class InviteUserForm(forms.Form):
    email = forms.CharField()

    # TODO: check if the user already exists


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]
