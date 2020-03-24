import requests
from progress.bar import ChargingBar

from pokebattle import celery_app

from .constants import POKE_API_URL
from .helpers import get_pokemon_from_api
from .models import Pokemon


@celery_app.task
def save_pokemon_task(poke_name):
    pokemon = Pokemon.objects.filter(name=poke_name).first()  # checks if pokemon already exists

    if pokemon:  # if it does, return it
        return pokemon

    data = get_pokemon_from_api(poke_name)  # otherwise, request this new pokemon

    # save and return new pokemon:
    return Pokemon.objects.create(
        poke_id=data["poke_id"],
        name=data["name"],
        defense=data["defense"],
        attack=data["attack"],
        hp=data["hp"],
    )


@celery_app.task
def get_all_pokemon_from_api_task():
    response = requests.get(f"{POKE_API_URL}/?limit=802")
    data = response.json()

    progress_bar = ChargingBar("Processing", max=802)
    for pokemon in data["results"]:
        save_pokemon_task.delay(pokemon["name"])
        progress_bar.next()
    progress_bar.finish()
