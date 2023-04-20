from django.shortcuts import render
from rest_framework import serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignupSerializer,LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User

# Create your views here.

class SignupView(APIView):
    permission_classes=[AllowAny] #any user,whether authenticated or not,is allowed to access the view.
    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)#it will return token and boolean value to neglect that boolean we use two variable
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        token=request.auth #  to get the user's authentication token
        token.delete()
        return Response({'message':'user logged out successfully'},status=status.HTTP_200_OK)

# class SignupViewSet(viewsets.ModelViewSet):
#     permission_classes=[IsAuthenticated]
#     serializer_class=SignupSerializer
#     queryset=User.objects.filter(id=0)
