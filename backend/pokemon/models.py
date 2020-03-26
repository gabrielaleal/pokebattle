from django.db import models  # noqa


class Pokemon(models.Model):
    poke_id = models.IntegerField(verbose_name="PokeAPI ID")
    name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=100, blank=True)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hp = models.IntegerField()

    class Meta:
        verbose_name_plural = "Pokemon"
        ordering = ("poke_id",)

    def __str__(self):
        return self.name
