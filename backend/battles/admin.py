from django.contrib import admin

from battles.utils.battle import run_battle_and_send_result_email  # noqa

from .models import Battle, BattleTeam  # noqa


class BattleAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)


class BattleTeamAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        run_battle_and_send_result_email(obj)


admin.site.register(Battle, BattleAdmin)
admin.site.register(BattleTeam, BattleTeamAdmin)
