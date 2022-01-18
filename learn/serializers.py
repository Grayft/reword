from rest_framework.serializers import ModelSerializer
from .models import UserCard, UserCategory


class BasicCardCategorySerializer(ModelSerializer):
    class Meta:
        abstract = True
        model = UserCategory
        fields = ('id', 'owner', 'name', 'slug')
        read_only_fields = ('owner', 'slug')


class BasicCardSerializer(ModelSerializer):
    class Meta:
        model = UserCard
        fields = ('id', 'ru_word', 'en_word', 'status',
                  'remain_repeated_count')
        read_only_fields = ('status', 'remain_repeated_count')


class CardCategoryRetrieveSerializer(BasicCardCategorySerializer, ModelSerializer):
    cards = BasicCardSerializer(many=True)

    class Meta(BasicCardCategorySerializer.Meta):
        fields = ('id', 'owner', 'name', 'slug', 'cards')