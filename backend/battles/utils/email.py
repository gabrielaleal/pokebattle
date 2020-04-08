from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

from templated_email import send_templated_mail


def send_battle_result(battle):
    battle_detail_path = reverse("battles:battle-detail", args=(battle.pk,))
    battle_details_url = urljoin(settings.HOST, battle_detail_path)
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


def send_opponent_battle_invitation_email(url, battle):
    send_templated_mail(
        template_name="battle_invite",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.opponent.email],
        context={
            "battle_id": battle.id,
            "battle_creator": battle.creator.email.split("@")[0],
            "battle_opponent": battle.opponent.email.split("@")[0],
            "select_battle_team_url": url,
        },
    )


def send_user_invite_to_pokebattle(url, user_invited_email, user_invitee_email):
    send_templated_mail(
        template_name="new_user_invite",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[user_invited_email],
        context={
            "user_who_invited": user_invitee_email.split("@")[0],
            "user_invited": user_invited_email.split("@")[0],
            "signup_url": url,
        },
    )
