from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Enforce password validation against Django's built-in rules
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserPublicSerializer(serializers.ModelSerializer):
    """Used for displaying user info without sensitive fields."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']