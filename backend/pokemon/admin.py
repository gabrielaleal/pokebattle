from django.contrib import admin  # noqa

from .models import Pokemon  # noqa


class PokemonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pokemon, PokemonAdmin)
