from rest_framework import serializers

from api.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["mobile", "password", "username", "first_name"]
        extra_kwargs = {"password": {"write_only": True}}
