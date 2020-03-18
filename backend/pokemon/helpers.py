import requests

from .models import Pokemon


POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_all_pokemon_from_api():
    response = requests.get(f"{POKE_API_URL}/?limit=802")
    data = response.json()

    for pokemon in data["results"]:
        print(pokemon["name"])
        save_pokemon(pokemon["name"])


def get_pokemon(poke_name):
    response = requests.get(f"{POKE_API_URL}{poke_name}")
    data = response.json()
    return {
        "name": data["name"],
        "poke_id": data["id"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }


def pokemon_exists(poke_name):
    response = requests.head(f"{POKE_API_URL}{poke_name}")
    return response


def save_pokemon(poke_name):
    pokemon = Pokemon.objects.filter(name=poke_name).first()  # checks if pokemon already exists

    if pokemon:  # if it does, return it
        return pokemon

    data = get_pokemon(poke_name)  # otherwise, request this new pokemon

    # save and return new pokemon:
    return Pokemon.objects.create(
        poke_id=data["poke_id"],
        name=data["name"],
        defense=data["defense"],
        attack=data["attack"],
        hp=data["hp"],
    )


def pokemon_sum_valid(pokemon_names):
    poke_sum = 0
    for poke_name in pokemon_names:
        pokemon = Pokemon.objects.filter(name=poke_name).first()

        if pokemon:
            poke_sum += pokemon.attack + pokemon.defense + pokemon.hp
            continue

        pokemon = get_pokemon(poke_name)
        poke_sum += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]

    return poke_sum <= 600
