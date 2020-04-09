from django import forms
from django.contrib.auth.forms import UserCreationForm

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
