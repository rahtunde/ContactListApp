from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.conf import settings
import jwt


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serialiazer = UserSerializer(data =request.data )
        if serialiazer.is_valid():
            serialiazer.save()
            return Response(serialiazer.data, status=status.HTTP_201_CREATED)
        
        return Response(serialiazer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)
        
        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)

            serializer = UserSerializer(user)

            data = {
                'user': serializer.data, 'token': auth_token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({'details': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


    