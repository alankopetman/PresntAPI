from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from .models import Course, Section, Attendance
import ipdb
import re

from .models import UserProfile

class UserSerializer(UserDetailsSerializer):
    password = serializers.CharField(write_only=True)
    pid = serializers.CharField(
            source='userprofile.pid',
    )
    is_professor = serializers.BooleanField(
        source='userprofile.is_professor',
        default=False,
    )
    profile_image = serializers.ImageField(
        source='userprofile.profile_image',
        allow_null=True,
    )
    class Meta(UserDetailsSerializer.Meta):
        li = list(UserDetailsSerializer.Meta.fields)
        li.remove('username')
        tu = tuple(li)
        fields = tu + (
            'is_professor',
            'password',
            'profile_image',
            'pid',
        )
        write_only_fields = ('password',)

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile', None)  # Using our profile as the validated
        user = super(UserSerializer, self).create(validated_data)  # Using default user to create
        user.set_password(validated_data['password'])
        user.save()
        self.create_or_update_profile(user, profile_data)
        return user

    def create_or_update_profile(self, user, userprofile_data):
        user_profile, created = UserProfile.objects.get_or_create(user=user, defaults=userprofile_data)
        if not created and userprofile_data is not None:
            super(UserSerializer, self).update(user_profile, userprofile_data)

    def update(self, instance, validated_data):  # Allowing for updates to the custom fields
        profile_data = validated_data.pop('userprofile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

class CustomRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    pid = serializers.CharField()
    is_professor = serializers.BooleanField(default=False)

    def validate_email(self, email):
        email = super(CustomRegistrationSerializer, self).validate_email(email)
        if '@fiu.edu' not in email:
            raise serializers.ValidationError(
                ("This is not an FIU e-mail address.")
            )
        return email

    def validate(self, data):
        regx = re.compile('\d')
        data = super(CustomRegistrationSerializer, self).validate(data)
        if data['is_professor'] and regx.search(data['email']):
            raise serializers.ValidationError(
                ("User is not a professor.")
            )
        if not data['first_name'] or regx.search(data['first_name']):
            raise serializers.ValidationError(
                ("First name must not contain number and must not be empty.")
            )
        if not data['last_name'] or regx.search(data['last_name']):
            raise serializers.ValidationError(
                ("Last name must not contain number and must not be empty.")
            )
        if not data['pid'] or len(data['pid']) != 7:
            raise serializers.ValidationError(
                ("PID must be 7 digits")
            )
        if UserProfile.objects.filter(pid=data['pid']).exists():
            raise serializers.ValidationError(
                ("There is already a user with this PID.")
            )
        return data

    def get_cleaned_data(self):
        cleaned_data = super(CustomRegistrationSerializer, self).get_cleaned_data()
        cleaned_data.update({
                    'pid': self.data['pid'],
                    'is_professor': self.data['is_professor'],
                    'first_name': self.data['first_name'],
                    'last_name': self.data['last_name'],
        })
        return cleaned_data

    def save(self, request):
        new_user = super(CustomRegistrationSerializer, self).save(request)
        UserProfile.objects.get_or_create(
            user=new_user,
            pid=self.data['pid'],
            is_professor=self.data['is_professor'],
        )
        return new_user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
