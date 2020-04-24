from rest_framework import serializers

from pokemon.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = "__all__"


class PokemonWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ("name", "id")
