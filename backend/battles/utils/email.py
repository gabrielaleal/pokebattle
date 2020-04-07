from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail


def send_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email,
            "battle_opponent": battle.opponent.email,
            "battle_winner": battle.winner.email,
            "battle_id": battle.id,
            "creator_team": battle.creator.teams.filter(battle=battle.id).first(),
            "opponent_team": battle.opponent.teams.filter(battle=battle.id).first(),
        },
    )


def send_user_invite_to_pokebattle(user_invited_email, user_who_invited_email):
    signup_path = reverse_lazy("signup")
    signup_url = f"{settings.HOST}{signup_path}"
    send_templated_mail(
        template_name="new_user_invite",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[user_invited_email],
        context={
            "user_who_invited": user_who_invited_email.split("@")[0],
            "user_invited": user_invited_email.split("@")[0],
            "signup_url": signup_url,
        },
    )
