from django.contrib import admin

from .models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pokemon, PokemonAdmin)
