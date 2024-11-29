from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'email', 'password']

    def create(self,validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'
        read_only_fields=['owner']
