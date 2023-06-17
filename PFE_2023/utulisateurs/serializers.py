from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from utulisateurs.models import CentreDeVaccination
User = get_user_model()


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2ODM4NjUzLCJpYXQiOjE2ODY4MzUwNTMsImp0aSI6IjU4Y2UyYjI2ZjM2NjQ0NDhhYzY2MmEwYTE1NjFjZGU2IiwidXNlcl9pZCI6M30.BOWeK4dGQ3DRP4UA4cdoJFf0uTcj-BRb1rFQ1h40Sr8
#------------register-patient-sr-------#
class PatientSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(required=True)
    nni = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['phone_number', 'nni', 'password']
    
    def create(self, validated_data):
        email = f"patient{validated_data['nni']}@vaccination.mr"
        password = validated_data.pop('password')
        user = User.objects.create_user(
            email=email,
            phone_number=validated_data['phone_number'],
            nni=validated_data['nni']
        )
        user.set_password(password)
        user.save()
        return user
    
    
class CentreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CentreDeVaccination
        fields = ['longitude', 'latitude','nom']

