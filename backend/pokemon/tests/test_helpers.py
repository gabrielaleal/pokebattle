import requests_mock

from common.utils.tests import TestCaseUtils
from pokemon.constants import POKE_API_URL
from pokemon.helpers import get_all_pokemon_from_api
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
            "sprites": {"front_default": "testimageurl.com/1"},
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
            "sprites": {"front_default": "testimageurl.com/2"},
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
            poke_id=1, name="bulbasaur", img_url="testimageurl.com/1", attack=49, defense=49, hp=45,
        )
        self.assertTrue(queryset.exists())

        queryset = Pokemon.objects.filter(
            poke_id=2, name="ivysaur", img_url="testimageurl.com/2", attack=62, defense=63, hp=60,
        )
        self.assertTrue(queryset.exists())
