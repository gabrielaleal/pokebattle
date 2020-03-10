from django.conf.urls import url

from .views import CreateBattleView, OnGoingBattlesListView, SettledBattlesListView


app_name = "battles"

urlpatterns = [
    url(r"^create/$", CreateBattleView.as_view(), name="create-battle"),
    url(r"^settled-battles/$", SettledBattlesListView.as_view(), name="settled-battles-list"),
    url(r"^on-going-battles/$", OnGoingBattlesListView.as_view(), name="on-going-battles-list"),
]
