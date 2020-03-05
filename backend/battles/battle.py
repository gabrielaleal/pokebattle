from .email import send_battle_result  # noqa


def compare_pokemon_attack_and_defense(pokemon_1, pokemon_2):
    # pokemon_1 always attacks and pokemon_2 always defends
    return pokemon_1.attack > pokemon_2.defense


def get_pokemon_with_highest_hp(pokemon_1, pokemon_2):
    if pokemon_1.hp > pokemon_2.hp:
        return pokemon_1
    return pokemon_2


def get_battle_result(battle):
    creator_team = battle.creator.teams.filter(battle=battle).first()
    opponent_team = battle.opponent.teams.filter(battle=battle).first()

    # first two rounds:
    if compare_pokemon_attack_and_defense(
        creator_team.pokemon_1, opponent_team.pokemon_1
    ) and compare_pokemon_attack_and_defense(creator_team.pokemon_2, opponent_team.pokemon_2):
        return battle.creator

    if compare_pokemon_attack_and_defense(
        opponent_team.pokemon_1, creator_team.pokemon_1
    ) and compare_pokemon_attack_and_defense(opponent_team.pokemon_2, creator_team.pokemon_2):
        return battle.opponent

    # in case of draw:
    if (
        get_pokemon_with_highest_hp(creator_team.pokemon_3, opponent_team.pokemon_3)
        == creator_team.pokemon_3
    ):
        return battle.creator
    return battle.opponent


def run_battle_and_send_result_email(battle_team):
    battle = battle_team.battle
    battle.winner = get_battle_result(battle)
    battle.save()
    send_battle_result(battle)
