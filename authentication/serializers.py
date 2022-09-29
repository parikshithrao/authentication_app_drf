from .models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 100, min_length = 6, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username can only be alpha numeric')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)