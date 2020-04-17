from rest_framework.permissions import BasePermission, IsAuthenticated

from battles.models import Battle


class IsInBattle(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.creator, obj.opponent]


class IsBattleOpponent(BasePermission):
    message = "Only battle opponent is allowed."

    def has_permission(self, request, view):
        battle_pk = view.kwargs.get("pk", None)
        battle = Battle.objects.get(pk=battle_pk)
        return request.user == battle.opponent


class BattleIsOngoing(IsAuthenticated):
    message = "This battle is settled."

    def has_permission(self, request, view):
        battle_pk = view.kwargs.get("pk", None)
        battle = Battle.objects.get(pk=battle_pk)
        return battle.status == "ONGOING"
