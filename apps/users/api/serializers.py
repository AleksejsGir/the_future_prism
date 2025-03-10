# apps/users/api/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Подтверждение пароля")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'avatar_url', 'email_notifications')
        read_only_fields = ('id', 'username', 'avatar_url')

    def get_avatar_url(self, obj):
        return obj.get_avatar_url()