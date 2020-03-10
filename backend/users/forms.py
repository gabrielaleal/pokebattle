# from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     user_exists = User.objects.filter(email=self.cleaned_data["email"])
    #     if user_exists:
    #         raise forms.ValidationError(
    #             "Ops, the email you entered is already registered."
    # )
