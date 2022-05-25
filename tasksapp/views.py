from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from .models import ConverterString
from .serializers import ConverterStringSerializer


class ConverterStringViewSet(ModelViewSet):
    queryset = ConverterString.objects.all()
    serializer_class = ConverterStringSerializer

    def create(self, validated_data):
        return ConverterString(**validated_data)

    def update(self, instance, validated_data):
        instance.raw_string = validated_data.get('raw_string', instance.raw_string)
        instance.convert_string = validated_data.get('convert_string', instance.convert_string)
        return instance
