from django.contrib import admin

from .models import Battle  # noqa


# Register your models here.
class BattleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Battle, BattleAdmin)
