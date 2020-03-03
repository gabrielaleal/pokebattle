from django.conf import settings

from templated_email import send_templated_mail


def send_battle_result(battle):
    # import ipdb;ipdb.set_trace();
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.SERVER_EMAIL,  # change it
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email,
            "battle_oponent": battle.opponent.email,
            "battle_winner": battle.winner.email,
            "battle_id": battle.id,
        },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )