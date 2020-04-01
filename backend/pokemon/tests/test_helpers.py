import requests_mock

from common.utils.tests import TestCaseUtils
from pokemon.helpers import POKE_API_URL, get_all_pokemon_from_api
from pokemon.models import Pokemon


class PokemonHelpersTest(TestCaseUtils):
    @requests_mock.mock()
    def test_get_all_pokemon_from_api(self, mock_request):
        # test if get_all_pokemon_from_api called requests.get
        # with the right parameter
        response = {
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            ]
        }
        pokemon_1 = {
            "id": 1,
            "name": "bulbasaur",
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/\
                    PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
            "stats": [
                {"base_stat": 49},
                {"base_stat": 49},
                {"base_stat": 49},
                {"base_stat": 49},  # defense
                {"base_stat": 49},  # attack
                {"base_stat": 45},  # hp
            ],
        }
        pokemon_2 = {
            "id": 2,
            "name": "ivysaur",
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/\
                    PokeAPI/sprites/master/sprites/pokemon/2.png"
            },
            "stats": [
                {"base_stat": 49},
                {"base_stat": 49},
                {"base_stat": 49},
                {"base_stat": 63},  # defense
                {"base_stat": 62},  # attack
                {"base_stat": 60},  # hp
            ],
        }
        mock_request.get(f"{POKE_API_URL}?limit=802", json=response)
        mock_request.get(f"{POKE_API_URL}bulbasaur", json=pokemon_1)
        mock_request.get(f"{POKE_API_URL}ivysaur", json=pokemon_2)
        get_all_pokemon_from_api()

        queryset = Pokemon.objects.filter(
            name="bulbasaur",
            poke_id="1",
            img_url="https://raw.githubusercontent.com/\
                PokeAPI/sprites/master/sprites/pokemon/1.png",
            attack=49,
            defense=49,
            hp=45,
        )
        self.assertTrue(queryset.exists())

        queryset = Pokemon.objects.filter(
            name="ivysaur",
            poke_id="2",
            img_url="https://raw.githubusercontent.com/\
                PokeAPI/sprites/master/sprites/pokemon/2.png",
            attack=62,
            defense=63,
            hp=60,
        )
        self.assertTrue(queryset.exists())
