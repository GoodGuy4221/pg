from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Notes


class NotesModelSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Notes
        fields = ('user', 'title', 'body',)

    def create(self, validated_data):
        return Notes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
