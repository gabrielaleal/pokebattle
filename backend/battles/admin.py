from django.contrib import admin

from .models import Battle, BattleTeam  # noqa


class BattleAdmin(admin.ModelAdmin):
    pass


class BattleTeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Battle, BattleAdmin)
admin.site.register(BattleTeam, BattleTeamAdmin)
