from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from .models import ConverterString
from .serializers import ConverterStringModelSerializer


class ConverterStringViewSet(ModelViewSet):
    queryset = ConverterString.objects.all()
    serializer_class = ConverterStringModelSerializer
    permission_classes = (IsAuthenticated,)
    # будет предоставлять доступ только по ...
    # authentication_classes = (TokenAuthentication,)

    # @staticmethod
    # def create(validated_data):
    #     return ConverterString(**validated_data)
    #
    # @staticmethod
    # def update(instance, **validated_data):
    #     instance.raw_string = validated_data.get('raw_string', instance.raw_string)
    #     instance.convert_string = validated_data.get('convert_string', instance.convert_string)
    #     return instance
