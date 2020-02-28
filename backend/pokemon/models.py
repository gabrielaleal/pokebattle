from django.db import models  # noqa


class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hitpoints = models.IntegerField()
