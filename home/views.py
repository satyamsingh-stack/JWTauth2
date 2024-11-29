from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class Operation1(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if(serializer.is_valid()):
            email=serializer.validated_data['email']
            if(User.objects.filter(email=email).exists()):
                return Response("Email Already Exists",status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Operation2(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        try:
            user1=User.objects.get(username=username)
            if(user1.check_password(password)):
                refresh=RefreshToken.for_user(user1)
                return Response({
                    "refresh" : str(refresh),
                    "access" : str(refresh.access_token)
                },status=status.HTTP_201_CREATED)
            return Response("invalid password", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("NOT Found",status=status.HTTP_404_NOT_FOUND)

class Operation3(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=TaskSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Operation4(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        task=Task.objects.all()
        serializer=TaskSerializer(task,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class Operation5(APIView):
    permission_classes=[IsAuthenticated]

    def patch(self,request,pk):
        try:
            item=Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        
        serializer=TaskSerializer(item,data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    