from model_mommy import mommy
from rest_framework.test import APIClient, APITestCase


class APITestCaseUtils(APITestCase):
    def setUp(self):
        self.user_1 = mommy.make("users.User")
        self.user_2 = mommy.make("users.User")
        self.random_user = mommy.make("users.User")

        self.auth_client = APIClient()
        # authenticate user
        self.auth_client.force_authenticate(user=self.user_1)
