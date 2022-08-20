from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from backend.users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'password',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
