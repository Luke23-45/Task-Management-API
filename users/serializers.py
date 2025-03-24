from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True, write_only=True)  # write_only field
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # Include full_name in the fields so that it gets processed.
        fields = ('full_name', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                _('A user with this email address already exists. Please try with another email.')
            )
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        first_name, *last_name_parts = full_name.split()
        last_name = ' '.join(last_name_parts) if last_name_parts else ''

        user = User.objects.create_user(
            username=email,  # Using the email as the username
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = f"{user.first_name} {user.last_name}".strip()
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email__iexact=email).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError(_('Invalid credentials.'))
            else:
                raise serializers.ValidationError(_('Invalid credentials.'))
        else:
            raise serializers.ValidationError(_('Must include "email" and "password".'))

        self.user = user
        return data
