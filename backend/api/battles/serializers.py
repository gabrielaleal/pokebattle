from rest_framework import serializers

from battles.models import Battle


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = "__all__"


class CreateBattleSerializer(serializers.Serializer):  # noqa
    class Meta:
        model = Battle
        fields = "opponent"

    def create(self, validated_data):
        # TODO: attribute request.user to creator, set battle status and create battle team
        return Battle.objects.create(**validated_data)
