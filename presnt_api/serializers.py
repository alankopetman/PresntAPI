from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_image = serializers.URLField(
        source='profile.image',
        allow_null=True,
        allow_blank=True,
    )
    class Meta:
        model = User
        fields = (
            'id',
            'url',
            'password',
            'email',
            'full_name',
            'profile_image',
        )
        write_only_fields = ('password',)
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)  # Using our profile as the validated
        user = super(UserSerializer, self).create(validated_data)  # Using default user to create
        user.set_password(validated_data['password'])
        user.save()
        self.create_or_update_profile(user, profile_data)
        return user


