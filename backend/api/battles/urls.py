from django.conf.urls import url

from .endpoints import BattleDetailEndpoint, OngoingBattlesListEndpoint, SettledBattlesListEndpoint


app_name = "api"

urlpatterns = [
    url(r"^battle/(?P<pk>[-\w]+)/$", BattleDetailEndpoint.as_view(), name="battle-detail"),
    url(r"^settled-battles/$", SettledBattlesListEndpoint.as_view(), name="settled-battles-list"),
    url(r"^ongoing-battles/$", OngoingBattlesListEndpoint.as_view(), name="ongoing-battles-list"),
]
