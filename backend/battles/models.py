from django.db import models

from pokemon.models import Pokemon  # noqa
from users.models import User  # noqa


class Battle(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_opponent")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won_battles", null=True
    )

    def __str__(self):
        return f"Battle #{self.id}: {self.creator.email} X {self.opponent.email}"


class BattleTeam(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")

    pokemon_1 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="+")
    pokemon_2 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="+")
    pokemon_3 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="+")

    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        creator_name = self.creator.email.split("@")[0]
        return f"{creator_name}'s Battle {self.battle.id} Team"
