from rest_framework import serializers

from api.pokemon.serializers import PokemonSerializer, PokemonWinnerSerializer
from api.users.serializers import UserSerializer
from battles.models import Battle, BattleTeam
from battles.tasks import run_battle_and_send_result_email
from battles.utils.battle import get_round_winner
from battles.utils.email import send_opponent_battle_invitation_email
from pokemon.helpers import (
    are_pokemon_positions_repeated,
    pokemon_sum_valid,
    repeated_pokemon_in_teams,
    sort_pokemon_in_correct_position,
)
from users.models import User

from .fields import BattleUrlDefault


class SelectTeamSerializerMixin(serializers.ModelSerializer):
    pokemon_1_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    pokemon_2_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    pokemon_3_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)

    def validate(self, data):  # same as the clean method on form
        if are_pokemon_positions_repeated(data):
            raise serializers.ValidationError("Each Pokemon must have a unique position.")

        is_pokemon_sum_valid = pokemon_sum_valid(
            [data["pokemon_1"], data["pokemon_2"], data["pokemon_3"],]  # noqa
        )

        if not is_pokemon_sum_valid:
            raise serializers.ValidationError(
                "The sum of the Pokemon points can't be greater than 600."
            )

        return data


class BattleTeamSerializer(serializers.ModelSerializer):
    pokemon_1 = PokemonSerializer()
    pokemon_2 = PokemonSerializer()
    pokemon_3 = PokemonSerializer()

    class Meta:
        model = BattleTeam
        fields = ("pokemon_1", "pokemon_2", "pokemon_3")


class BattleSerializer(serializers.ModelSerializer):
    creator_team = serializers.SerializerMethodField()
    opponent_team = serializers.SerializerMethodField()
    matches_winners = serializers.SerializerMethodField()
    creator = UserSerializer()
    opponent = UserSerializer()
    winner = UserSerializer()

    def get_creator_team(self, obj):
        team = BattleTeam.objects.filter(battle=obj, creator=obj.creator).first()
        # if the creator team doesn't exist yet, just return user data
        if not team:
            return {}
        # if it exists, return the battle team data (which also has the creator information)
        serializer = BattleTeamSerializer(instance=team)
        return serializer.data

    def get_opponent_team(self, obj):
        team = BattleTeam.objects.filter(battle=obj, creator=obj.opponent).first()
        if not team:
            return {}
        serializer = BattleTeamSerializer(instance=team)
        return serializer.data

    def get_matches_winners(self, obj):
        if obj.status == "ONGOING":
            return {}
        creator_team = BattleTeam.objects.filter(battle=obj, creator=obj.creator).first()
        opponent_team = BattleTeam.objects.filter(battle=obj, creator=obj.opponent).first()
        creator_team_pokemon = [
            creator_team.pokemon_1,
            creator_team.pokemon_2,
            creator_team.pokemon_3,
        ]
        opponent_team_pokemon = [
            opponent_team.pokemon_1,
            opponent_team.pokemon_2,
            opponent_team.pokemon_3,
        ]

        winners = []

        for creator_pokemon, opponent_pokemon, position in zip(
            creator_team_pokemon, opponent_team_pokemon, [1, 2, 3]
        ):
            winner = get_round_winner(creator_pokemon, opponent_pokemon)
            serializer = PokemonWinnerSerializer(instance=winner)
            data = serializer.data
            data["position"] = position
            winners.append(data)
        return winners

    class Meta:
        model = Battle
        fields = (
            "timestamp",
            "status",
            "creator",
            "creator_team",
            "opponent_team",
            "opponent",
            "winner",
            "matches_winners",
            "id",
        )


class CreateBattleSerializer(SelectTeamSerializerMixin):
    opponent_id = serializers.PrimaryKeyRelatedField(
        source="battle.opponent", queryset=User.objects.all(),
    )
    # Read-only fields (so I can use them on frontend if I need any of them)
    opponent = UserSerializer(source="battle.opponent", read_only=True)
    creator = UserSerializer(source="battle.creator", read_only=True)
    winner = UserSerializer(source="battle.winner", read_only=True)
    status = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(source="battle.timestamp", read_only=True)
    battle_id = serializers.PrimaryKeyRelatedField(source="battle.id", read_only=True)

    class Meta:
        model = BattleTeam
        fields = (
            "opponent",
            "opponent_id",
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
            "timestamp",
            "creator",
            "status",
            "winner",
            "battle_id",
        )

    def create(self, validated_data):  # same as the form_valid method on the view
        # get self.request
        request = self.context.get("request")

        # create battle first
        battle_data = validated_data.pop("battle")

        battle_data["creator"] = request.user
        battle = Battle.objects.create(**battle_data)

        battle_team_data = sort_pokemon_in_correct_position(validated_data)
        battle_team_data["battle"] = battle
        battle_team_data["creator"] = request.user

        instance = super().create(battle_team_data)

        send_opponent_battle_invitation_email(battle)

        return instance


class SelectOpponentTeamSerializer(SelectTeamSerializerMixin):
    battle = serializers.HiddenField(default=BattleUrlDefault())

    class Meta:
        model = BattleTeam
        fields = (
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
            "battle",
        )

    def validate(self, data):
        data = super().validate(data)
        pokemon = [
            data["pokemon_1"],
            data["pokemon_2"],
            data["pokemon_3"],
        ]
        if repeated_pokemon_in_teams(pokemon, data["battle"]):
            raise serializers.ValidationError(
                "You chose a Pokemon from your opponent's team. Try again."
            )
        return data

    def create(self, validated_data):
        # get self.request
        request = self.context.get("request")

        battle_team_data = sort_pokemon_in_correct_position(validated_data)
        battle_team_data["battle"] = validated_data["battle"]
        battle_team_data["creator"] = request.user

        instance = super().create(battle_team_data)

        run_battle_and_send_result_email.delay(instance.battle.id)

        return instance
