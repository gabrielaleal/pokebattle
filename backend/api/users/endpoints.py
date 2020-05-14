from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User

from .serializers import UserSerializer


class UserAuthenticatedEndpoint(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        obj = self.request.user
        return obj


class OpponentsList(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.exclude(email=user.email)
        return queryset
