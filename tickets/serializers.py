from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "description",
            "type",
            "author",
        )
        model = Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username",)


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(email=validated_data['email'],
                                               username=validated_data['username']
                                               )
        user.set_password(validated_data['password'])
        user.save()
        return user
