from django.test import TestCase
from rest_framework import serializers,status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import Serializer
# Create your tests here.
    
class SignupSerializer(Serializer):
    username=serializers.CharField(max_length=20)
    first_name=serializers.CharField(max_length=20)
    last_name=serializers.CharField(max_length=20)
    email=serializers.EmailField()
    password=serializers.CharField(max_length=50,write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('username already exists')
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email id already registered')
        return value
    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        password=validated_data['password']
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user,role=UserProfile.CUSTOMER)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    