from unittest.mock import Mock, patch  # noqa

from common.utils.tests import TestCaseUtils
from pokemon.helpers import POKE_API_URL, get_all_pokemon_from_api  # noqa


class PokemonHelpersTest(TestCaseUtils):
    @patch("pokemon.helpers.requests")
    @patch("pokemon.helpers.ChargingBar")
    def test_get_all_pokemon_from_api(self, mock_requests):
        pass
        # import ipdb; ipdb.set_trace()
        # mock_requests.get(POKE_API_URL).return_value
