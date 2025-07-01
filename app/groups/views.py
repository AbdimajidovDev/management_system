from rest_framework import viewsets

from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from app.users.utility import *


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperAdmin | IsAdmin]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

