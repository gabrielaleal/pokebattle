from django.conf.urls import url

from .views import (
    BattleDetailView,
    CreateBattleView,
    OnGoingBattlesListView,
    SettledBattlesListView,
)


app_name = "battles"

urlpatterns = [
    url(r"^create/$", CreateBattleView.as_view(), name="create-battle"),
    url(r"^settled-battles/$", SettledBattlesListView.as_view(), name="settled-battles-list"),
    url(r"^ongoing-battles/$", OnGoingBattlesListView.as_view(), name="ongoing-battles-list"),
    url(r"^(?P<pk>[-\w]+)/$", BattleDetailView.as_view(), name="battle-detail"),
]
