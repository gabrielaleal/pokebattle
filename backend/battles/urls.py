from django.conf.urls import url

from .views import CreateBattleView  # noqa


app_name = "battles"

urlpatterns = [
    url(r"^create/$", CreateBattleView.as_view(), name="create-battle"),
]
