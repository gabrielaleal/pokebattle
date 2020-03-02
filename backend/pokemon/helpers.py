import requests

from .models import Pokemon  # noqa


POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(poke_id):
    response = requests.get(f"{POKE_API_URL}{poke_id}")
    data = response.json()
    return {
        "name": data["name"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }


def pokemon_exists(poke_id):
    response = requests.head(f"{POKE_API_URL}{poke_id}")
    return response


def save_pokemon(poke_id):
    pokemon = Pokemon.objects.filter(poke_id=poke_id).first()  # checks if pokemon already exists

    if pokemon:  # if it does, return it
        return pokemon

    data = get_pokemon(poke_id)  # otherwise, request this new pokemon

    # save and return new pokemon:
    return Pokemon.objects.create(
        poke_id=poke_id,
        name=data["name"],
        defense=data["defense"],
        attack=data["attack"],
        hp=data["hp"],
    )


def pokemon_sum_valid(pokemon_ids):
    poke_sum = 0
    for poke_id in pokemon_ids:
        pokemon = Pokemon.objects.filter(poke_id=poke_id).first()

        if pokemon:
            poke_sum += pokemon.attack + pokemon.defense + pokemon.hp
            continue

        pokemon = get_pokemon(poke_id)
        poke_sum += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]

    return poke_sum <= 600
