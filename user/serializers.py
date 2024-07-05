from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationValidationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise serializers.ValidationError()

class CodeValidationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=6)

class UserAuthenticationValidationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()