import requests

from .models import Pokemon  # noqa


POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(poke_id):
    response = requests.get(f"{POKE_API_URL}{poke_id}")
    # data = response.json()
    # response.status_code may be useful to treat data
    return response


def save_pokemon(poke_id):
    pokemon = Pokemon.objects.filter(poke_id=poke_id).first()  # checks if pokemon already exists

    if pokemon:  # if it does, return it
        return pokemon

    response = get_pokemon(poke_id)  # otherwise, request this new pokemon

    data = response.json()

    defense = data["stats"][3]["base_stat"]
    attack = data["stats"][4]["base_stat"]
    hp = data["stats"][5]["base_stat"]

    # save and return new pokemon:
    return Pokemon.objects.create(
        poke_id=poke_id, name=data["name"], defense=defense, attack=attack, hitpoints=hp
    )
