from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # this serializer is used to return an object instead of
    # an id whenever it's used as a form field
    class Meta:
        model = User
        fields = ("email",)
