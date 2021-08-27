from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CardCategory, Card


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'ru_word', 'en_word', 'status', 'categories',
                  'remain_repeated_count')
        read_only_fields = ('status', 'remain_repeated_count', 'category')

    def get_fields(self):
        fields = super(CardSerializer, self).get_fields()

        auth_user_pk = self.context.get('request').user.pk
        fields['categories'].child_relation.queryset = \
            CardCategory.objects.filter(owner__pk=auth_user_pk)
        return fields


class CardCategorySerializer(ModelSerializer):
    class Meta:
        model = CardCategory
        fields = ('id', 'owner', 'name', 'slug')
        read_only_fields = ('owner', 'slug')


class CardCategoryRetrieveSerializer(CardCategorySerializer):
    class Meta:
        model = CardCategory
        fields = ('id', 'owner', 'name', 'slug')

