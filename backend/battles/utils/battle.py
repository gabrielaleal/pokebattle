from .email import send_battle_result


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


def get_player_team(battle, player):
    team = getattr(battle, player).teams.filter(battle=battle).first()
    return [team.pokemon_1, team.pokemon_2, team.pokemon_3]


def count_wins(creator_team, opponent_team):
    creator_wins, opponent_wins = 0, 0

    for (creator_pokemon, opponent_pokemon) in zip(creator_team, opponent_team):
        if get_round_winner(creator_pokemon, opponent_pokemon) == creator_pokemon:
            creator_wins += 1
        else:
            opponent_wins += 1

    return creator_wins, opponent_wins


def get_battle_winner(battle):
    creator_team = get_player_team(battle, "creator")
    opponent_team = get_player_team(battle, "opponent")

    creator_wins, opponent_wins = count_wins(creator_team, opponent_team)

    if creator_wins > opponent_wins:
        return battle.creator
    return battle.opponent


def run_battle_and_send_result_email(battle_team):
    battle = battle_team.battle
    battle.winner = get_battle_winner(battle)
    battle.status = "SETTLED"
    battle.save()
    send_battle_result(battle)
