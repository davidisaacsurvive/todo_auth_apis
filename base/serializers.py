from rest_framework import serializers
from base.models import Todo, Location
from django.contrib.auth import get_user_model

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            # username= validated_data.get('email'),  # Use email as username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user

class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['user', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['created_at']