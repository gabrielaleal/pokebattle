from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail


def send_battle_result(battle):
    battle_detail_path = reverse_lazy("battles:battle-detail", args=(battle.pk,))
    battle_details_url = f"{settings.HOST}{battle_detail_path}"
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email.split("@")[0],
            "battle_opponent": battle.opponent.email.split("@")[0],
            "battle_winner": battle.winner.email.split("@")[0],
            "battle_id": battle.id,
            "creator_team": battle.creator.teams.filter(battle=battle.id).first(),
            "opponent_team": battle.opponent.teams.filter(battle=battle.id).first(),
            "battle_details_url": battle_details_url,
        },
    )


def send_opponent_battle_invitation_email(battle):
    select_battle_team_path = reverse_lazy("battles:select-team", args=(battle.pk,))
    select_battle_team_url = f"{settings.HOST}{select_battle_team_path}"
    send_templated_mail(
        template_name="battle_invite",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.opponent.email],
        context={
            "battle_id": battle.id,
            "battle_creator": battle.creator.email.split("@")[0],
            "battle_opponent": battle.opponent.email.split("@")[0],
            "select_battle_team_url": select_battle_team_url,
        },
    )
