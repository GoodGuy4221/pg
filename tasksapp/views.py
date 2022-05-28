from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.views import APIView

from .models import ConverterString
from .serializers import ConverterStringModelSerializer
from services import character_count_converter_1


class CharacterCountConverterAPIView(APIView):

    def get(self, request):
        raw_string = request.query_params.get('raw_string', '')
        if raw_string:
            response = ConverterString.objects.filter(raw_string=raw_string)
            if response:
                return Response({'convert_string': response.first().convert_string, })
            else:
                convert_string = character_count_converter_1(raw_string)
                ConverterString.objects.create(raw_string=raw_string, convert_string=convert_string)
                return Response({'convert_string': convert_string, })


class ConverterStringAPIView(ModelViewSet):
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
