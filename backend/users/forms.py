from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import User


class InviteUserForm(forms.Form):
    email = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]

        # check if email already exists
        if User.objects.check_if_email_already_exists(email):
            raise forms.ValidationError("The email you entered is from an existing user.")

        return cleaned_data


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]


class LoginForm(AuthenticationForm):
    error_messages = {"invalid_login": ("Please enter a correct %(username)s and password.")}
