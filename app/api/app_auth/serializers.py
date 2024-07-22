from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    """
    Serializer for authentication
    """

    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating new User objects
    """

    class Meta:
        model = User
        fields = ["name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, Any]):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, value: str) -> str:
        """
        Validate password to be at least 8 character longs, contain a special character and at least a number
        """
        import re

        MIN_LENGTH = 8
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(
                f"Password must be at least {MIN_LENGTH} characters long"
            )

        # We use regex here because its the fastest and the best way to achieve our functionality
        # in efficient way
        #
        # we would match against password entry against a pattern containing at least a number and
        # a special character
        PASSWORD_REGEX = r"^(?=.*[0-9])(?=.*[!@#$%^&*])"
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                f"Password must contain at least one number and one special character"
            )
        return value
