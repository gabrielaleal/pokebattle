from django.contrib import admin

from .battle import run_battle  # noqa
from .models import Battle, BattleTeam  # noqa


class BattleAdmin(admin.ModelAdmin):
    pass


class BattleTeamAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        run_battle(obj)


admin.site.register(Battle, BattleAdmin)
admin.site.register(BattleTeam, BattleTeamAdmin)
