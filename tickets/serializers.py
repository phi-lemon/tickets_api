from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers

from .models import Project, Contributor, Issue


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=get_user_model().objects.all()
     )

    class Meta:
        model = Contributor
        fields = ('id', 'user')


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    project = serializers.StringRelatedField()

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('project',)


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
