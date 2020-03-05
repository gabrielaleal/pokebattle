from django.conf import settings

from templated_email import send_templated_mail  # noqa


def send_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email,
            "battle_oponent": battle.opponent.email,
            "battle_winner": battle.winner.email,
            "battle_id": battle.id,
        },
    )
