from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            role=validated_data.get('role', User.USER),
        )
        if validated_data.get('role') == User.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'bio', 'role',
        ]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        username = self.initial_data.get('username')
        email_exists = User.objects.filter(
            username=username,
            email=value
        ).exists()

        if not email_exists:
            raise ValidationError('This email already exists')

        return value

    class Meta:
        model = User
        fields = ['email']


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    email = serializers.EmailField()

    def validate_confirmation_code(self, value):
        email = self.initial_data.get('email', '')
        if email:
            response_code = make_password(
                password=email, salt=None, hasher='default'
            )
            if response_code != value:
                raise ValidationError('The confirmation code is not correct')
        return value
