from .email import send_battle_result  # noqa


def win_attack(pokemon_1, pokemon_2):  # pokemon_1 always attacks and pokemon_2 always defends
    if pokemon_1.attack > pokemon_2.defense:
        return True
    return False


def highest_hp_pokemon(pokemon_1, pokemon_2):
    if pokemon_1.hp > pokemon_2.hp:
        return pokemon_1
    return pokemon_2


def get_battle_result(battle):
    creator_team = battle.creator.teams.filter(battle=battle).first()
    opponent_team = battle.creator.teams.filter(battle=battle).first()

    # first two rounds:
    if win_attack(creator_team.pokemon_1, opponent_team.pokemon_1) and win_attack(
        creator_team.pokemon_2, opponent_team.pokemon_2
    ):
        return battle.creator

    if win_attack(opponent_team.pokemon_1, creator_team.pokemon_1) and win_attack(
        opponent_team.pokemon_2, creator_team.pokemon_2
    ):
        return battle.opponent

    # in case of draw:
    if (
        highest_hp_pokemon(creator_team.pokemon_3, opponent_team.pokemon_3)
        == creator_team.pokemon_3
    ):
        return battle.creator
    return battle.opponent


def run_battle(battle_team):
    battle = battle_team.battle
    battle.winner = get_battle_result(battle)
    battle.save()
    send_battle_result(battle)
    print("done!")
