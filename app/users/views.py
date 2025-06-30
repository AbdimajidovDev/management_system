from rest_framework import viewsets
from app.users.models import User
from app.users.serializers import CreateUserSerializer
from app.users.utility import IsSuperAdmin


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperAdmin,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
