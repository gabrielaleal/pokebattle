from celery.utils.log import get_task_logger

from pokebattle import celery_app

from .models import Battle
from .utils.battle import get_battle_winner
from .utils.email import send_battle_result


logger = get_task_logger(__name__)


@celery_app.task
def run_battle_and_send_result_email(battle_id):
    logger.info("About to solve Battle %d", battle_id)
    battle = Battle.objects.get(id=battle_id)
    battle.winner = get_battle_winner(battle)
    battle.status = "SETTLED"
    battle.save()
    logger.info("Solved Battle %d", battle_id)
    send_battle_result(battle)
