from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'avatar', 'phone_number', 'city']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'city']
