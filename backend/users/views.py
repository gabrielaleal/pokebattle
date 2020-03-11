from django.contrib import messages  # noqa
from django.contrib.auth import authenticate, login  # noqa
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("home")
    template_name = "signup.html"

    # def form_valid(self, form):
    #     new_user = form.save()
    #     messages.info(self.request, "Thanks for registering. You are now logged in.")
    #     new_user = authenticate(
    #         email=form.cleaned_data["email"], password=form.cleaned_data["password1"],
    #     )
    #     if new_user is not None:
    #         login(self.request, new_user)
    #     else:
    #         messages.info(request, "Sorry, did you register correctly?")
    #     return super().form_valid(form)
