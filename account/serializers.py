from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from .models import *
from django.contrib.auth.models import Group

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('mobileNo', 'image')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id','url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.mobileNo = profile_data.get('mobileNo', profile.mobileNo)
        profile.image = profile_data.get('image', profile.image)
        profile.save()

        return instance

class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','email','password')
		extra_kwargs = {'password': {'write_only': True},'id':{'read_only':True}}
	
	def validate_password(self, value):
		try:
			validate_password(value)
		except exceptions.ValidationError as exc:
			raise serializers.ValidationError(str(exc))
		return value

	def create(self, validated_data):
		group = Group.objects.get(name='Customer')
		password=validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		user.groups.add(group)
		return user