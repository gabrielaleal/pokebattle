from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"

    def form_valid(self, form):
        new_user = form.save()
        new_user = authenticate(
            email=form.cleaned_data["email"], password=form.cleaned_data["password1"],
        )
        if new_user is not None:
            login(self.request, new_user)
            messages.info(self.request, "Thanks for registering. You are now logged in.")
        else:
            messages.info(self.request, "Sorry, did you register correctly?")
        return super().form_valid(form)
