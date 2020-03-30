from django.contrib.messages import get_messages

from model_mommy import mommy

from battles.models import Battle, BattleTeam
from common.utils.tests import TestCaseUtils


class CreateBattleViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = mommy.make("users.User", email="opponent@email.com")

    def test_create_battle_successfully(self):
        pokemon_1, pokemon_2, pokemon_3 = (
            mommy.make("pokemon.Pokemon", name="pikachu", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="bulbasaur", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="charizard", attack=60, defense=45, hp=50),
        )
        battle_data = {
            "opponent": self.opponent.id,
            "pokemon_1": pokemon_1.id,
            "pokemon_2": pokemon_2.id,
            "pokemon_3": pokemon_3.id,
        }

        response = self.auth_client.post(self.reverse("battles:create-battle"), battle_data)
        self.assertResponse302(response)

        message = list(get_messages(response.wsgi_request))[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(
            message.message,
            f"<h5>Your battle against <b>{self.opponent.email}</b> was created!</h5>"
            f"<div>Round 1: <b>{pokemon_1.name}</b> - Attack: \
            {pokemon_1.attack} | Defense: {pokemon_1.defense} \
            | HP: {pokemon_1.hp}</div>"
            f"<div>Round 2: <b>{pokemon_2.name}</b> - Attack: \
            {pokemon_2.attack} | Defense: {pokemon_2.defense} \
            | HP: {pokemon_2.hp}</div>"
            f"<div>Round 3: <b>{pokemon_3.name}</b> - Attack: \
            {pokemon_3.attack} | Defense: {pokemon_3.defense} \
            | HP: {pokemon_3.hp}</div>"
            f"<div style='margin-top: 10px;'>Now wait for your opponent to fight back!</div>",
        )

        self.assertTrue(
            Battle.objects.filter(
                creator=self.user, opponent=self.opponent, status="ONGOING"
            ).exists()
        )

        self.assertTrue(
            BattleTeam.objects.filter(
                creator=self.user, pokemon_1=pokemon_1, pokemon_2=pokemon_2, pokemon_3=pokemon_3
            ).exists()
        )

    def test_if_pokemon_sum_valid_fails(self):
        pokemon_1, pokemon_2, pokemon_3 = (
            mommy.make("pokemon.Pokemon", attack=100, defense=100, hp=100),
            mommy.make("pokemon.Pokemon", attack=50, defense=50, hp=50),
            mommy.make("pokemon.Pokemon", attack=50, defense=50, hp=51),
        )
        battle_data = {
            "opponent": self.opponent.id,
            "pokemon_1": pokemon_1.id,
            "pokemon_2": pokemon_2.id,
            "pokemon_3": pokemon_3.id,
        }

        response = self.auth_client.post(self.reverse("battles:create-battle"), battle_data)
        self.assertResponse200(response)

        form = response.context["form"]
        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["__all__"], ["The sum of the Pokemon points can't be greater than 600."]
        )


class SelectOpponentTeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.creator = mommy.make("users.User")
        self.opponent = mommy.make("users.User")

        self.matching_battle = mommy.make(  # noqa
            "battles.Battle", pk=1, creator=self.creator, opponent=self.opponent, status="ONGOING"
        )

        self.opponent_pokemon_1, self.opponent_pokemon_2, self.opponent_pokemon_3 = (
            mommy.make("pokemon.Pokemon", name="pikachu", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="bulbasaur", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="charizard", attack=60, defense=45, hp=50),
        )
        self.opponent_pokemon_team = {
            "pokemon_1": self.opponent_pokemon_1.id,
            "pokemon_2": self.opponent_pokemon_2.id,
            "pokemon_3": self.opponent_pokemon_3.id,
        }

        self.creator_pokemon_1, self.creator_pokemon_2, self.creator_pokemon_3 = (
            mommy.make("pokemon.Pokemon", name="ivysaur", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="pikipek", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", name="roselia", attack=60, defense=45, hp=50),
        )

    def test_if_not_matching_battle_pk_fails(self):
        response = self.auth_client.post(self.reverse("battles:select-team", pk=1))
        self.assertResponse404(response)

    def test_if_page_context_data_is_correct(self):
        # test if context["page_title"] returns what I expect it to
        self.auth_client.force_login(self.opponent)
        response = self.auth_client.get(self.reverse("battles:select-team", pk=1))
        self.assertEqual(
            response.context["page_title"], f"Select Battle #{self.matching_battle.pk} Team"
        )

    def test_if_not_matching_status_fails(self):
        not_matching_battle = mommy.make(  # noqa
            "battles.Battle", pk=1, creator=self.creator, opponent=self.opponent, status="SETTLED"
        )
        self.auth_client.force_login(self.opponent)

        response = self.auth_client.post(self.reverse("battles:select-team", pk=1))
        self.assertResponse404(response)

    def test_if_not_matching_opponent_fails(self):
        not_matching_battle = mommy.make(  # noqa
            "battles.Battle", pk=1, creator=self.creator, opponent=self.opponent, status="ONGOING"
        )

        self.auth_client.force_login(self.creator)
        response = self.auth_client.post(self.reverse("battles:select-team", pk=1))
        self.assertResponse404(response)

    def test_if_not_matching_opponent_and_status_fails(self):
        not_matching_battle = mommy.make(  # noqa
            "battles.Battle", pk=1, creator=self.creator, opponent=self.opponent, status="SETTLED"
        )

        self.auth_client.force_login(self.creator)

        response = self.auth_client.post(self.reverse("battles:select-team", pk=1))
        self.assertResponse404(response)

    def test_if_matching_opponent_and_status_success(self):
        creator_pokemon_team = mommy.make(  # noqa
            "battles.BattleTeam",
            creator=self.creator,
            battle=self.matching_battle,
            pokemon_1=self.creator_pokemon_1,
            pokemon_2=self.creator_pokemon_2,
            pokemon_3=self.creator_pokemon_3,
        )

        self.auth_client.force_login(self.opponent)
        response = self.auth_client.post(
            self.reverse("battles:select-team", pk=1), self.opponent_pokemon_team
        )
        self.assertResponse302(response)

        # test if client is redirected to the correct page
        self.assertEqual(response.url, self.reverse("battles:battle-detail", pk=1))

    def test_if_opponent_team_has_pokemon_from_creator_team(self):
        # check if opponent didn't choose a pokemon from the creator team
        creator_pokemon_team = mommy.make(  # noqa
            "battles.BattleTeam",
            creator=self.creator,
            battle=self.matching_battle,
            pokemon_1=self.opponent_pokemon_1,
            pokemon_2=self.creator_pokemon_2,
            pokemon_3=self.creator_pokemon_3,
        )

        self.auth_client.force_login(self.opponent)
        response = self.auth_client.post(
            self.reverse("battles:select-team", pk=1), self.opponent_pokemon_team
        )
        self.assertResponse200(response)

        form = response.context["form"]
        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["__all__"], ["You chose a Pokemon from your opponent's team. Try again."]
        )

    def test_if_battle_values_change(self):
        # test if the battle values change (its status and winner)
        # after running run_battle_and_send_result_email
        self.creator_pokemon_team = mommy.make(  # noqa
            "battles.BattleTeam",
            creator=self.creator,
            battle=self.matching_battle,
            pokemon_1=self.creator_pokemon_1,
            pokemon_2=self.creator_pokemon_2,
            pokemon_3=self.creator_pokemon_3,
        )

        self.auth_client.force_login(self.opponent)
        response = self.auth_client.post(
            self.reverse("battles:select-team", pk=1), self.opponent_pokemon_team, follow=True
        )

        battle = response.context_data["battle"]
        self.assertEqual(battle.status, "SETTLED")
        self.assertIsNotNone(battle.winner)
