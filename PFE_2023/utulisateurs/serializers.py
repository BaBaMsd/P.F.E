from rest_framework import serializers
from django.contrib.auth.models import User
#from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator , qs_exists
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

'''class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'nni']'''

class PatientSerializer(serializers.ModelSerializer):
   # profile = ProfileSerializer()

    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    
    nni = serializers.CharField(
        required = True,
        validators = [
            UniqueValidator(
            queryset= User.objects.all(),

                
            )
            
            
        ]
    )

    email = serializers.EmailField(
        required = True,
        validators= [
            UniqueValidator(
                queryset= User.objects.all(),
                
            )
        ]
    )
    

    class Meta:
        model = User
        fields = ['id','nni','email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(email=validated_data['email'])
        user.set_password(password)
        user.save()
        return user

'''  def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        profile = instance.profile
        profile.role = profile_data.get('role', profile.role)
        profile.nni = profile_data.get('nni', profile.nni)
        profile.save()
        return instance '''