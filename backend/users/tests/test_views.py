from unittest.mock import patch

from django.conf import settings
from django.contrib.messages import get_messages
from django.test import Client

from model_mommy import mommy

from common.utils.tests import TestCaseUtils


class SignUpViewTest(TestCaseUtils):
    def test_logged_in_user_should_be_redirected_to_home(self):
        response = self.auth_client.get(self.reverse("signup"))
        self.assertResponse302(response)
        self.assertEqual(response.url, self.reverse("home"))

    def test_user_signed_up_successfully(self):
        client = Client()
        client_credentials = {
            "email": "newuser@vinta.com.br",
            "password1": "123456",
            "password2": "123456",
        }
        response = client.post(self.reverse("signup"), client_credentials)
        self.assertResponse200(response)


class InviteUserViewTest(TestCaseUtils):
    def test_invite_user_successfully(self):
        form_data = {"email": "newuser@test.com"}
        response = self.auth_client.post(self.reverse("invite-user"), form_data)
        self.assertResponse302(response)

        message = list(get_messages(response.wsgi_request))[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(
            message.message,
            "Thank you! We've sent an email inviting <b>newuser@test.com</b> to join us.",
        )

    def test_if_entering_existing_email_fails(self):
        # create user
        existing_user = mommy.make("users.User", email="existinguser@test.com")  # noqa

        # invite existing user
        form_data = {"email": "existinguser@test.com"}

        response = self.auth_client.post(self.reverse("invite-user"), form_data)
        self.assertResponse200(response)

        form = response.context["form"]
        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["__all__"], ["The email you entered is from an existing user."]
        )

    @patch("battles.utils.email.send_templated_mail")
    def test_if_invitation_email_is_sent(self, mock_templated_mail):
        form_data = {"email": "newuser@test.com"}
        self.auth_client.post(self.reverse("invite-user"), form_data)

        signup_path = self.reverse("signup")
        mock_templated_mail.assert_called_with(
            template_name="new_user_invite",
            from_email=settings.EMAIL_ADDRESS,
            recipient_list=[form_data["email"]],
            context={
                "user_who_invited": self.user.email.split("@")[0],
                "user_invited": form_data["email"].split("@")[0],
                "signup_url": f"{settings.HOST}{signup_path}",
            },
        )
