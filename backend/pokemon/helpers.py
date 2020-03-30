import requests
from progress.bar import ChargingBar

from .models import Pokemon


POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_all_pokemon_from_api():
    response = requests.get(f"{POKE_API_URL}/?limit=802")
    data = response.json()

    progress_bar = ChargingBar("Processing", max=802)
    for pokemon in data["results"]:
        save_pokemon(pokemon["name"])
        progress_bar.next()
    progress_bar.finish()


def get_pokemon_from_api(poke_name):
    response = requests.get(f"{POKE_API_URL}{poke_name}")
    data = response.json()
    return {
        "poke_id": data["id"],
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }


def pokemon_exists_in_api(poke_name):
    response = requests.head(f"{POKE_API_URL}{poke_name}")
    return bool(response)


def save_pokemon(poke_name):
    pokemon = Pokemon.objects.filter(name=poke_name).first()  # checks if pokemon already exists

    if pokemon:  # if it does, return it
        return pokemon

    data = get_pokemon_from_api(poke_name)  # otherwise, request this new pokemon

    # save and return new pokemon:
    return Pokemon.objects.create(
        poke_id=data["poke_id"],
        name=data["name"],
        img_url=data["img_url"],
        defense=data["defense"],
        attack=data["attack"],
        hp=data["hp"],
    )


def pokemon_sum_valid(pokemon_names):
    poke_sum = 0
    for poke_name in pokemon_names:
        pokemon = Pokemon.objects.filter(name=poke_name).first()

        poke_sum += pokemon.attack + pokemon.defense + pokemon.hp

    return poke_sum <= 600


def repeated_pokemon_in_teams(opponent_pokemon, battle):
    creator_team = battle.creator.teams.filter(battle=battle.id).first()
    creator_pokemon = [creator_team.pokemon_1, creator_team.pokemon_2, creator_team.pokemon_3]
    if set(creator_pokemon) & set(opponent_pokemon):
        return True
    return False


def sort_pokemon_in_correct_position(data):
    pokemon = dict()

    for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
        key = "pokemon_" + str(data[field + "_position"])
        pokemon[key] = data[field]
    return pokemon


def are_pokemon_positions_repeated(fields):
    # filters only by positions
    positions = [value for field, value in fields.items() if field.endswith("_position")]

    # returns new set with duplicates removed
    positions_set = set(positions)
    return len(positions_set) != len(positions)
