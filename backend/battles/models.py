from django.db import models

from users.models import User  # noqa


# Create your models here.
class Battle(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_opponent")

    # def __str__(self):
    #     return f"{self.creator.email} X {self.opponent.email}"
