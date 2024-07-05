from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import RegistrationValidationSerializer,CodeValidationSerializer,UserAuthenticationValidationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import randint
from django.utils import timezone
from .models import Code
from rest_framework.generics import CreateAPIView

class RegistrationView(CreateAPIView):
    def post(self, request,*args, **kwargs):
        serializer = RegistrationValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = int(('').join([str(randint(0, 9)) for i in range(6)]))
        dedline = timezone.now() + timezone.timedelta(minutes=5)
        Code.objects.create(user=user, code=code, deadline=dedline)
        return Response(data=code, status=status.HTTP_201_CREATED)

class Confirm(CreateAPIView):
    def post(self,request,*args, **kwargs):
        serializer = CodeValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_code = Code.objects.get(code=serializer.validated_data['code'])
        except Code.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user_code.deadline < timezone.now():
            code = int(('').join([str(randint(0, 9)) for i in range(6)]))
            dedline = timezone.now() + timezone.timedelta(minutes=5)
            Code.objects.create(user=request.user, code=code, deadline=dedline)
            user_code.delete()
            return Response(data=f'dedline reached,new code {code}', status=status.HTTP_201_CREATED)
        user_code.user.is_active = True
        user_code.user.save()
        user_code.delete()
        return Response(status=status.HTTP_200_OK)

class LoginView(CreateAPIView):
    def post(self,request,*args, **kwargs):
        serializer = UserAuthenticationValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'error': 'user does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def register(request):
#     serializer = RegistrationValidationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data['username']
#     password = serializer.validated_data['password']
#     user=User.objects.create_user(username=username, password=password,is_active=False)
#     code = int(('').join([str(randint(0, 9)) for i in range(6)]))
#     dedline=timezone.now()+timezone.timedelta(minutes=5)
#     Code.objects.create(user=user, code=code, deadline=dedline)
#     return Response(data=code, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def confirm(request):
#     serializer = CodeValidationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     try:
#         user_code=Code.objects.get(code=serializer.validated_data['code'])
#     except Code.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if user_code.deadline<timezone.now():
#         code = int(('').join([str(randint(0, 9)) for i in range(6)]))
#         dedline=timezone.now()+timezone.timedelta(minutes=5)
#         Code.objects.create(user=request.user, code=code, deadline=dedline)
#         user_code.delete()
#         return Response(data=f'dedline reached,new code {code}',status=status.HTTP_201_CREATED)
#     user_code.user.is_active=True
#     user_code.user.save()
#     user_code.delete()
#     return Response(status=status.HTTP_200_OK)



# @api_view(['POST'])
# def authentication_api_view(request):
    # serializer = UserAuthenticationValidationSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    #
    # user=authenticate(**serializer.validated_data)
    # if user:
    #     token,created=Token.objects.get_or_create(user=user)
    #     return Response(data={'key':token.key})
    # return Response(data={'error':'user does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
