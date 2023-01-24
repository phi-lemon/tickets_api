from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers

from .models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "description",
            "type",
            "author",
        )

    def create(self, validated_data):
        author = self.context['request'].user
        project = Project.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author=author,
        )
        project.save()
        return project


class UsersListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ('user',)


class UsersCreateSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()  # readonly

    class Meta:
        model = Contributor
        fields = ('user', 'project')


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password", "first_name", "last_name"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
