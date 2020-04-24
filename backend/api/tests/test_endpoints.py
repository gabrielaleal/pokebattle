from unittest.mock import patch
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

from model_mommy import mommy

from api.battles.serializers import BattleSerializer
from api.common.utils.tests import APITestCaseUtils
from battles.models import Battle, BattleTeam
from battles.tests.mixins import MakePokemonMixin


class CreateBattleEndpointTest(APITestCaseUtils):
    def setUp(self):
        super().setUp()
        self.pokemon_1 = mommy.make("pokemon.Pokemon", attack=50, defense=60, hp=40)
        self.pokemon_2 = mommy.make("pokemon.Pokemon", attack=50, defense=50, hp=40)
        self.pokemon_3 = mommy.make("pokemon.Pokemon", attack=40, defense=50, hp=50)

    # test pokemon sum
    def test_if_pokemon_sum_valid_fails(self):
        pokemon_1 = mommy.make("pokemon.Pokemon", attack=50, defense=100, hp=100)
        pokemon_2 = mommy.make("pokemon.Pokemon", attack=50, defense=100, hp=100)
        pokemon_3 = mommy.make("pokemon.Pokemon", attack=100, defense=50, hp=50)
        form_data = {
            "opponent_id": self.user_2.id,
            "pokemon_1": pokemon_1.id,
            "pokemon_1_position": 1,
            "pokemon_2": pokemon_2.id,
            "pokemon_2_position": 2,
            "pokemon_3": pokemon_3.id,
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(reverse("api:create-battle"), form_data)
        self.assertEqual(response.status_code, 400)
        message = response.json().get("non_field_errors")[0]
        self.assertEqual(message, "The sum of the Pokemon points can't be greater than 600.")

    # test pokemon unique position
    def test_if_pokemon_repeated_position_fails(self):
        form_data = {
            "opponent_id": self.user_2.id,
            "pokemon_1": self.pokemon_1.id,
            "pokemon_1_position": 1,
            "pokemon_2": self.pokemon_2.id,
            "pokemon_2_position": 1,
            "pokemon_3": self.pokemon_3.id,
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(reverse("api:create-battle"), form_data)
        self.assertEqual(response.status_code, 400)
        message = response.json().get("non_field_errors")[0]
        self.assertEqual(message, "Each Pokemon must have a unique position.")

    def test_create_battle_successfully(self):
        form_data = {
            "opponent_id": self.user_2.id,
            "pokemon_1": self.pokemon_1.id,
            "pokemon_1_position": 1,
            "pokemon_2": self.pokemon_2.id,
            "pokemon_2_position": 3,
            "pokemon_3": self.pokemon_3.id,
            "pokemon_3_position": 2,
        }
        response = self.auth_client.post(reverse("api:create-battle"), form_data)
        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Battle.objects.filter(
                creator=self.user_1, opponent=self.user_2, status="ONGOING"
            ).exists()
        )

        self.assertTrue(
            BattleTeam.objects.filter(
                creator=self.user_1,
                pokemon_1=self.pokemon_1,
                pokemon_2=self.pokemon_3,
                pokemon_3=self.pokemon_2,
            ).exists()
        )

    @patch("battles.utils.email.send_templated_mail")
    def test_if_battle_invitation_email_is_sent(self, mock_templated_mail):
        form_data = {
            "opponent_id": self.user_2.id,
            "pokemon_1": self.pokemon_1.id,
            "pokemon_1_position": 1,
            "pokemon_2": self.pokemon_2.id,
            "pokemon_2_position": 3,
            "pokemon_3": self.pokemon_3.id,
            "pokemon_3_position": 2,
        }

        self.auth_client.post(reverse("api:create-battle"), form_data)

        battle = Battle.objects.filter(
            creator=self.user_1, opponent=self.user_2, status="ONGOING"
        ).first()

        battle_path = reverse("battles:select-team", args=(battle.pk,))

        mock_templated_mail.assert_called_with(
            template_name="battle_invite",
            from_email=settings.EMAIL_ADDRESS,
            recipient_list=[self.user_2.email],
            context={
                "battle_id": battle.id,
                "battle_creator": self.user_1.email.split("@")[0],
                "battle_opponent": self.user_2.email.split("@")[0],
                "select_battle_team_url": urljoin(settings.HOST, battle_path),
            },
        )


class SelectOpponentTeamEndpointTest(MakePokemonMixin, APITestCaseUtils):
    def setUp(self):
        super().setUp()
        self.matching_battle = mommy.make(  # noqa
            "battles.Battle", pk=1, creator=self.user_1, opponent=self.user_2, status="ONGOING"
        )
        self.user_1_pokemon_1, self.user_1_pokemon_2, self.user_1_pokemon_3 = self._make_pokemon()
        self.user_2_pokemon_1, self.user_2_pokemon_2, self.user_2_pokemon_3 = self._make_pokemon()

        self.user_1_pokemon_team = mommy.make(  # battle creator team
            "battles.BattleTeam",
            creator=self.user_1,
            battle=self.matching_battle,
            pokemon_1=self.user_1_pokemon_1,
            pokemon_2=self.user_1_pokemon_2,
            pokemon_3=self.user_1_pokemon_3,
        )

    def test_if_opponent_team_has_pokemon_from_creator_team(self):
        # check if opponent didn't choose a pokemon from the creator team
        form_data = {  # battle opponent team
            "pokemon_1": self.user_1_pokemon_1.id,
            "pokemon_2": self.user_2_pokemon_2.id,
            "pokemon_3": self.user_2_pokemon_3.id,
            "pokemon_1_position": 1,
            "pokemon_2_position": 2,
            "pokemon_3_position": 3,
        }

        self.auth_client.force_authenticate(self.user_2)
        response = self.auth_client.post(
            reverse("api:select-team", args=(self.matching_battle.pk,)), form_data
        )
        self.assertEqual(response.status_code, 400)

        message = response.json().get("non_field_errors")[0]
        self.assertEqual(message, "You chose a Pokemon from your opponent's team. Try again.")

    def test_if_not_matching_status_fails(self):
        # permission test
        battle = mommy.make(
            "battles.Battle", pk=2, creator=self.random_user, opponent=self.user_1, status="SETTLED"
        )
        response = self.auth_client.post(reverse("api:select-team", args=(battle.pk,)))
        self.assertEqual(response.status_code, 403)
        message = response.json().get("detail")
        self.assertEqual(message, "This battle is settled.")

    def test_if_not_matching_opponent_fails(self):
        response = self.auth_client.post(
            reverse("api:select-team", args=(self.matching_battle.pk,))
        )
        self.assertEqual(response.status_code, 403)
        message = response.json().get("detail")
        self.assertEqual(message, "Only battle opponent is allowed.")

    def test_create_battle_team_successfully(self):
        self.auth_client.force_authenticate(user=self.user_2)
        form_data = {
            "pokemon_1": self.user_2_pokemon_1.id,
            "pokemon_2": self.user_2_pokemon_2.id,
            "pokemon_3": self.user_2_pokemon_3.id,
            "pokemon_1_position": 1,
            "pokemon_2_position": 2,
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("api:select-team", args=(self.matching_battle.pk,)), form_data
        )
        self.assertEqual(response.status_code, 201)

        # check if battle status and winner values changes
        self.matching_battle.refresh_from_db()
        self.assertTrue(self.matching_battle.status, "SETTLED")
        self.assertIsNotNone(self.matching_battle.winner)

    @patch("battles.utils.email.send_templated_mail")
    def test_if_battle_result_email_is_being_sent(self, mock_templated_mail):
        self.auth_client.force_authenticate(user=self.user_2)
        form_data = {
            "pokemon_1": self.user_2_pokemon_1.id,
            "pokemon_2": self.user_2_pokemon_2.id,
            "pokemon_3": self.user_2_pokemon_3.id,
            "pokemon_1_position": 1,
            "pokemon_2_position": 2,
            "pokemon_3_position": 3,
        }
        self.auth_client.post(
            reverse("api:select-team", args=(self.matching_battle.pk,)), form_data
        )

        self.matching_battle.refresh_from_db()
        battle_path = reverse("battles:battle-detail", args=(self.matching_battle.pk,))
        mock_templated_mail.assert_called_with(
            template_name="battle_result",
            from_email=settings.EMAIL_ADDRESS,
            recipient_list=[self.user_1.email, self.user_2.email],
            context={
                "battle_creator": self.user_1.email.split("@")[0],
                "battle_opponent": self.user_2.email.split("@")[0],
                "battle_winner": self.matching_battle.winner.email.split("@")[0],
                "battle_id": self.matching_battle.id,
                "creator_team": self.matching_battle.creator.teams.filter(
                    battle=self.matching_battle.id
                ).first(),
                "opponent_team": self.matching_battle.opponent.teams.filter(
                    battle=self.matching_battle.id
                ).first(),
                "battle_details_url": urljoin(settings.HOST, battle_path),
            },
        )


class SettledBattlesListEndpointTest(APITestCaseUtils):
    def setUp(self):
        super().setUp()
        # created battles that will match or not according to the test case
        self.battle_1 = mommy.make(
            "battles.Battle",
            creator=self.user_1,
            opponent=self.user_2,
            status="SETTLED",
            pk=1,
            winner=self.user_1,
        )
        self.battle_2 = mommy.make(
            "battles.Battle",
            creator=self.user_1,
            opponent=self.user_2,
            status="SETTLED",
            pk=2,
            winner=self.user_2,
        )
        self.battle_3 = mommy.make(
            "battles.Battle", creator=self.user_1, opponent=self.user_2, status="ON_GOING", pk=3
        )
        self.battle_4 = mommy.make(
            "battles.Battle",
            creator=self.random_user,
            opponent=self.user_2,
            status="SETTLED",
            pk=4,
            winner=self.random_user,
        )

    def test_matching_queryset_success(self):
        response = self.auth_client.get(reverse("api:settled-battles-list"))
        self.assertEqual(response.status_code, 200)

        matching_battles = BattleSerializer([self.battle_1, self.battle_2], many=True)
        # the battles returned must be the ones settled with the user logged
        # in as the creator or the opponent
        self.assertEqual(
            matching_battles.data, response.json(),
        )

        # the ongoing battle and the battle where the user authenticated isn't
        # creator nor opponent must not be in the battle list
        not_matching_battles = BattleSerializer([self.battle_3, self.battle_4], many=True)
        self.assertNotIn(not_matching_battles.data, response.json())


class OngoingBattlesListEndpointTest(APITestCaseUtils):
    def setUp(self):
        super().setUp()
        self.battle_1 = mommy.make(
            "battles.Battle", creator=self.user_1, opponent=self.user_2, status="ONGOING"
        )
        self.battle_2 = mommy.make(
            "battles.Battle", creator=self.user_1, opponent=self.user_2, status="SETTLED"
        )
        self.battle_3 = mommy.make(
            "battles.Battle", creator=self.user_2, opponent=self.random_user, status="ONGOING"
        )
        self.battle_4 = mommy.make(
            "battles.Battle", creator=self.user_2, opponent=self.user_1, status="ONGOING"
        )

    def test_matching_queryset_success(self):
        response = self.auth_client.get(reverse("api:ongoing-battles-list"))
        self.assertEqual(response.status_code, 200)

        matching_battles = BattleSerializer([self.battle_1, self.battle_4], many=True)
        self.assertEqual(matching_battles.data, response.json())

        not_matching_battles = BattleSerializer([self.battle_2, self.battle_3], many=True)
        self.assertNotIn(not_matching_battles.data, response.json())


class BattleDetailEndpointTest(APITestCaseUtils):
    def test_if_user_not_in_battle_fails(self):
        battle = mommy.make("battles.Battle", pk=1, creator=self.user_1, opponent=self.user_2)

        self.auth_client.force_authenticate(user=self.random_user)

        response = self.auth_client.get(reverse("api:battle-detail", args=(battle.pk,)))
        self.assertEqual(response.status_code, 403)
