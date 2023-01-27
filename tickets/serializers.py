from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    contributors = serializers.StringRelatedField(many=True, read_only=True)

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
    assignee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=get_user_model().objects.all()
     )

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    issue = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True
     )

    class Meta:
        model = Comment
        fields = '__all__'


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
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
