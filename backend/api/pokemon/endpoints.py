from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from pokemon.models import Pokemon

from .serializers import PokemonSerializer


class ListPokemons(ListAPIView):
    serializer_class = PokemonSerializer
    queryset = Pokemon.objects.all()
    permission_classes = (IsAuthenticated,)
