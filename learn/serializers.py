from rest_framework.serializers import ModelSerializer
from .models import CardCategory, Card


class CardCategorySerializer(ModelSerializer):
    class Meta:
        model = CardCategory
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug', )


class CardSerializer(ModelSerializer):
    categories = CardCategorySerializer(many=True)

    class Meta:
        model = Card
        fields = ('id', 'ru_word', 'en_word', 'status', 'categories',
                  'remain_repeated_count')
