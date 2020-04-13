from django.conf.urls import url

from .endpoints import (
    BattleDetailEndpoint,
    CreateBattleEndpoint,
    OngoingBattlesListEndpoint,
    SettledBattlesListEndpoint,
)


app_name = "api"

urlpatterns = [
    url(r"^battle/(?P<pk>[-\w]+)/$", BattleDetailEndpoint.as_view(), name="battle-detail"),
    url(r"^create-battle/$", CreateBattleEndpoint.as_view(), name="create-battle"),
    url(r"^settled-battles/$", SettledBattlesListEndpoint.as_view(), name="settled-battles-list"),
    url(r"^ongoing-battles/$", OngoingBattlesListEndpoint.as_view(), name="ongoing-battles-list"),
]
