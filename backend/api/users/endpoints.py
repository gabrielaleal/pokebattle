from rest_framework.generics import RetrieveAPIView

from .serializers import UserSerializer


class UserAuthenticatedEndpoint(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        obj = self.request.user
        return obj
