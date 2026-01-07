from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
            "updated_at",
            "credits",
            "user_permissions",
        )

        read_only_fields = (
            "id",
            "email",
            "username",
            "is_staff",
            "date_joined",
            "updated_at",
            "credits",
            "user_permissions",
        )

# For logout
class EmptySerializer(serializers.Serializer):
    pass