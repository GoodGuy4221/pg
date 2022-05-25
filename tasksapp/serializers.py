from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from .models import ConverterString


class ConverterStringModelSerializer(ModelSerializer):
    class Meta:
        model = ConverterString
        fields = (
            'pk',
            'raw_string',
            'convert_string',
        )
