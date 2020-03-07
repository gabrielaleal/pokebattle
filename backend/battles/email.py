from django.conf import settings

from templated_email import send_templated_mail  # noqa


def send_battle_result(battle):
    # import ipdb; ipdb.set_trace()
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email,
            "battle_oponent": battle.opponent.email,
            "battle_winner": battle.winner.email,
            "battle_id": battle.id,
            "creator_team": battle.creator.teams.filter(battle=battle.id).first(),
            "opponent_team": battle.opponent.teams.filter(battle=battle.id).first(),
        },
    )
