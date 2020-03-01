from django.db import models  # noqa


class Pokemon(models.Model):
    poke_id = models.IntegerField(verbose_name="PokeAPI ID")
    name = models.CharField(max_length=50)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hitpoints = models.IntegerField()

    class Meta:
        verbose_name_plural = "Pokemon"

    def __str__(self):
        return self.name
