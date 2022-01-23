from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework import serializers
from .models import UserCard, UserCategory
from django.contrib.auth.models import User


class DisplaySerializerChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        return self._choices[value]


class BaseUserCategorySerializer(ModelSerializer):
    class Meta:
        abstract = True
        model = UserCategory
        fields = ('id', 'owner', 'name', 'slug', 'is_selected')
        read_only_fields = ('owner', 'slug')


class UserCardSerializer(ModelSerializer):
    status = DisplaySerializerChoiceField(choices=UserCard.card_statuses)

    class Meta:
        model = UserCard
        fields = ('id', 'ru_word', 'en_word', 'transcription', 'examples',
                  'status', 'count_repeated')
        read_only_fields = ('id', 'status', 'count_repeated')


class UserCategoryRetrieveSerializer(BaseUserCategorySerializer,
                                     ModelSerializer):
    cards = UserCardSerializer(many=True)

    class Meta(BaseUserCategorySerializer.Meta):
        fields = ('id', 'owner', 'name', 'slug', 'cards')


class LoginRequestSerializer(Serializer):
    username = CharField(max_length=100)
    password = CharField(max_length=100, min_length=4)
