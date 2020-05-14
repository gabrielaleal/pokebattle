from django.conf.urls import url

from .battles.endpoints import (
    BattleDetailEndpoint,
    CreateBattleEndpoint,
    OngoingBattlesListEndpoint,
    SelectOpponentTeamEndpoint,
    SettledBattlesListEndpoint,
)
from .pokemon.endpoints import ListPokemons
from .users.endpoints import OpponentsList, UserAuthenticatedEndpoint


urlpatterns = [
    # battles' urls
    url(r"^battles/create/$", CreateBattleEndpoint.as_view(), name="create-battle"),
    url(
        r"^battles/select-team/(?P<pk>[-\w]+)/$",
        SelectOpponentTeamEndpoint.as_view(),
        name="select-team",
    ),
    url(r"^battles/settled/$", SettledBattlesListEndpoint.as_view(), name="settled-battles-list"),
    url(r"^battles/ongoing/$", OngoingBattlesListEndpoint.as_view(), name="ongoing-battles-list"),
    url(r"^battles/(?P<pk>[-\w]+)/$", BattleDetailEndpoint.as_view(), name="battle-detail"),
    # users urls
    url(r"^users/authenticated/$", UserAuthenticatedEndpoint.as_view(), name="user-authenticated"),
    url(r"^users/opponents/$", OpponentsList.as_view(), name="opponents-list"),
    # pokemon's urls
    url(r"^pokemon/list/$", ListPokemons.as_view(), name="pokemon-list"),
]
