from .email import send_battle_result  # noqa


def compare_pokemon_attack_and_defense(pokemon_1, pokemon_2):
    # pokemon_1 always attacks and pokemon_2 always defends
    if pokemon_1.attack > pokemon_2.defense:
        return pokemon_1
    return pokemon_2


def get_pokemon_with_highest_hp(pokemon_1, pokemon_2):
    if pokemon_1.hp > pokemon_2.hp:
        return pokemon_1
    return pokemon_2


def get_round_winner(c_pokemon, o_pokemon):
    # c_pokemon stands for the creator's pokemon
    # o_pokemon stands for the opponents's pokemon
    if compare_pokemon_attack_and_defense(
        c_pokemon, o_pokemon
    ) == compare_pokemon_attack_and_defense(o_pokemon, c_pokemon):
        return compare_pokemon_attack_and_defense(c_pokemon, o_pokemon)
    return get_pokemon_with_highest_hp(c_pokemon, o_pokemon)


def get_battle_winner(battle):
    creator_team = battle.creator.teams.filter(battle=battle).first()
    opponent_team = battle.opponent.teams.filter(battle=battle).first()

    c_poke_team = [  # creator's team
        creator_team.pokemon_1,
        creator_team.pokemon_2,
        creator_team.pokemon_3,
    ]

    o_poke_team = [  # opponent's team
        opponent_team.pokemon_1,
        opponent_team.pokemon_2,
        opponent_team.pokemon_3,
    ]

    rounds_winners = []

    for (c_pokemon, o_pokemon) in zip(c_poke_team, o_poke_team):
        if get_round_winner(c_pokemon, o_pokemon) == c_pokemon:
            rounds_winners.append("creator")
        else:
            rounds_winners.append("opponent")

    if rounds_winners.count("creator") > rounds_winners.count("opponent"):
        return battle.creator
    return battle.opponent


def run_battle_and_send_result_email(battle_team):
    battle = battle_team.battle
    battle.winner = get_battle_winner(battle)
    battle.save()
    send_battle_result(battle)
