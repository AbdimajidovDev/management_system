from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.models import User
from app.users.serializers import CreateUserSerializer, LoginSerializer
from app.users.permissions import IsSuperAdmin, IsAdminOrSuperAdmin


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperAdmin,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

@extend_schema(tags=['login'])
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# @extend_schema(tags=[''])
class TeacherListView(generics.ListAPIView):
    queryset = User.objects.filter(role='t')
    serializer_class = CreateUserSerializer
    permission_classes = (IsAdminOrSuperAdmin,)

