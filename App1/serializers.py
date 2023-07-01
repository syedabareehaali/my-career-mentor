from rest_framework import serializers
from .models import User, Score

# # User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# # Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'country', 'city')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'],
            validated_data['country'], 
            validated_data['city']
            )


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
