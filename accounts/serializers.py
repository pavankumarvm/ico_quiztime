from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class IcoUserSerializer(serializers.ModelSerializer):
    """
        Serialize the User Data
    """

    password = serializers.CharField(write_only=True, required= False)
    class Meta:
        model = UserModel
        fields = ['email', 'password','first_name', 'last_name', 'date_joined', 'last_login', 'is_admin' ,'is_active']
        read_only_fields = ['date_joined', 'last_login']

    def create(self, validated_data):
        return UserModel.objects.create(**validated_data)