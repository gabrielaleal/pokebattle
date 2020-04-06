from django.contrib import admin

from battles.tasks import run_battle_and_send_result_email

from .models import Battle, BattleTeam


class BattleAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)


class BattleTeamAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        run_battle_and_send_result_email.delay(obj.battle.id)


admin.site.register(Battle, BattleAdmin)
admin.site.register(BattleTeam, BattleTeamAdmin)
