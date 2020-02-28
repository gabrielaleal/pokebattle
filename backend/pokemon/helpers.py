import requests

from .models import Pokemon  # noqa


POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(name):
    response = requests.get(f"{POKE_API_URL}{name.lower()}")
    data = response.json()
    # response.status_code may be useful to treat data
    return data


def save_pokemon(name):
    data = get_pokemon(name)

    pokemon = Pokemon.objects.filter(
        name__iexact=name
    ).first()  # __iexect makes name case insensitive (database lookups)

    if pokemon:
        return pokemon

    defense = data["stats"][3]["base_stat"]
    attack = data["stats"][4]["base_stat"]
    hp = data["stats"][5]["base_stat"]

    return Pokemon.objects.create(name=data["name"], defense=defense, attack=attack, hitpoints=hp)
