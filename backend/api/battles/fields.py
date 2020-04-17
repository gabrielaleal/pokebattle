from api.common.fields import UrlFieldDefault  # noqa
from battles.models import Battle


class BattleUrlDefault(UrlFieldDefault):
    model = Battle
    url_id_name = "pk"
