from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(max_length=100)
    invite_code = serializers.CharField(required=False)

    class Meta:
        model= User
        fields= ['username', 'email', 'password', 'confirm_password', 'invite_code']
        write_only = ["password", "confirm_password"]


    def create(self, validated_data):
        if validated_data["password"] == validated_data["confirm_password"]:
             return User.objects.create_user(
                username=validated_data["username"], password=validated_data["password"]
                )

"""
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        read_only = ["referral_code"]
        fields = (
            "id",
            "user",
            "avatar",
            "country",
            "phone_number",
            "referral_code",
            "total_referrals",
        )
"""
       
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer()
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "last_name",
            "is_active",
            #"profile",
        )
        
    """
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create profile related to the user
        if profile_data:
            profile_instance, _ = Profile.objects.update_or_create(user=instance, defaults=profile_data)
            # Update profile instance with nested serializer data
            ProfileSerializer(profile_instance, data=profile_data, partial=True).is_valid(raise_exception=True)
            profile_instance.save()
        return instance
    """


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True,write_only=True)
    new_password = serializers.CharField(required=True,write_only=True)
    confirm_new_password= serializers.CharField(required=True,write_only=True)