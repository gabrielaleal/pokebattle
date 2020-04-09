from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views import generic

from battles.utils.email import send_user_invite_to_pokebattle

from .forms import InviteUserForm, SignUpForm


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


class InviteUserView(LoginRequiredMixin, generic.FormView):
    template_name = "invite_user.html"
    form_class = InviteUserForm
    success_url = reverse_lazy("invite-user")

    def form_valid(self, form):
        user_invited_email = form.cleaned_data["email"]
        user_invitee_email = self.request.user.email
        send_user_invite_to_pokebattle(user_invited_email, user_invitee_email)

        success_message = format_html(
            f"Thank you! We've sent an email inviting <b>{user_invited_email}</b> to join us."
        )
        messages.success(self.request, success_message)

        return super().form_valid(form)
