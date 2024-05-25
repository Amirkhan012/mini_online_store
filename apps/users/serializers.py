from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        """
        Создание нового пользователя.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.USER
        )
        user.is_email_verified = False
        user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]


class ResendActivationEmailSerializer(serializers.Serializer):
    """
    Сериализатор для повторной отправки активационного письма.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Валидация email для повторной отправки активационного письма.
        """
        try:
            user = User.objects.get(email=value)
            if user.is_email_verified:
                raise serializers.ValidationError(
                    "Email is already verified."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist."
            )
        return value


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Валидация данных для входа пользователя.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if not user.is_email_verified:
                    raise serializers.ValidationError(
                        'Email is not verified.'
                    )
            else:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )

        data['user'] = user
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)
    blacklist = serializers.BooleanField(default=False)
