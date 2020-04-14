from django.urls import reverse

from model_mommy import mommy
from rest_framework.test import APIClient, APITestCase


class SettledBattlesListEndpointTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.creator = mommy.make("users.User")
        self.opponent = mommy.make("users.User")
        self.random_user = mommy.make("users.User")
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.creator)

        # created battles that will match or not according to the test case
        self.battle_1 = mommy.make(
            "battles.Battle", creator=self.creator, opponent=self.opponent, status="SETTLED", pk=1
        )
        self.battle_2 = mommy.make(
            "battles.Battle", creator=self.creator, opponent=self.opponent, status="SETTLED", pk=2
        )
        self.battle_3 = mommy.make(
            "battles.Battle", creator=self.creator, opponent=self.opponent, status="ON_GOING", pk=3
        )
        self.battle_4 = mommy.make(
            "battles.Battle",
            creator=self.creator,
            opponent=self.random_user,
            status="SETTLED",
            pk=4,
        )

    def test_matching_queryset_success(self):
        response = self.auth_client.get(reverse("api:settled-battles-list"))
        assert response.status_code == 200

        # # the battles returned must be the ones settled with the user logged
        # # in as the creator or the opponent
        # assertEqual(
        #     set([self.battle_1, self.battle_2, self.battle_4]),
        #     set(response.context_data["battle_list"]),
        # )

        # # the ongoing battle must not be in the battle list
        # assertNotIn(
        #     set([self.battle_3]), set(response.context_data["battle_list"]),
        # )
