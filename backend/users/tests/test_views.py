from django.test import Client

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
