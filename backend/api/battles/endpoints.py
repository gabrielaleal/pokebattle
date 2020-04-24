from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from battles.models import Battle

from .permissions import BattleIsOngoing, IsBattleOpponent, IsInBattle
from .serializers import (
    BattleDetailsSerializer,
    BattleSerializer,
    CreateBattleSerializer,
    SelectOpponentTeamSerializer,
)


class CreateBattleEndpoint(CreateAPIView):
    serializer_class = CreateBattleSerializer
    permission_classes = (IsAuthenticated,)


class SelectOpponentTeamEndpoint(CreateAPIView):
    serializer_class = SelectOpponentTeamSerializer
    permission_classes = (
        IsBattleOpponent,
        BattleIsOngoing,
    )


class BattleDetailEndpoint(RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleDetailsSerializer
    permission_classes = (IsInBattle,)


class SettledBattlesListEndpoint(ListAPIView):
    serializer_class = BattleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Battle.objects.filter(Q(creator=user) | Q(opponent=user)).filter(
            status="SETTLED"
        )
        return queryset


class OngoingBattlesListEndpoint(ListAPIView):
    serializer_class = BattleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Battle.objects.filter(Q(creator=user) | Q(opponent=user)).filter(
            status="ONGOING"
        )
        return queryset
