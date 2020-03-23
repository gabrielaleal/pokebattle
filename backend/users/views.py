from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("home")
    template_name = "auth/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get("email"), form.cleaned_data.get("password1")
        new_user = authenticate(email=email, password=password)
        if new_user is not None:
            login(self.request, new_user)
        else:
            messages.info(self.request, "Sorry, did you register correctly?")
        return valid


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "auth/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")
