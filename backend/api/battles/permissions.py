from rest_framework.permissions import IsAuthenticated


class IsInBattle(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.creator, obj.opponent]
