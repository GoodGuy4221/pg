from rest_framework.serializers import ModelSerializer

from .models import ConverterString


class ConverterStringSerializer(ModelSerializer):
    class Meta:
        model = ConverterString
        fields = (
            'raw_string',
            'convert_string',
        )
