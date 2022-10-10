from dataclasses import field
from rest_framework.exceptions import AuthenticationFailed 
from .models import User
from rest_framework import serializers
from django.contrib import auth

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

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length = 50, min_length = 6, write_only = True)
    username = serializers.CharField(max_length = 100, read_only = True)
    tokens = serializers.CharField(max_length = 50, min_length = 6, read_only = True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email = email, password = password)

        if not user:
            raise AuthenticationFailed('Register your email')

        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, Contact Admin')

        if not user.is_verified:
            raise AuthenticationFailed('Verify your account')

        


        return {
            'email' : user.email,
            'username' : user.username,
            'tokens' : user.tokens()
        } 



