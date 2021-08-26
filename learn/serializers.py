from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import CardCategory, Card


class CardCategorySerializer(ModelSerializer):
    class Meta:
        model = CardCategory
        fields = ('id', 'owner', 'name', 'slug')
        read_only_fields = ('owner', 'slug')


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'ru_word', 'en_word', 'status', 'categories',
                  'remain_repeated_count')
        read_only_fields = ('status', 'remain_repeated_count', 'category')

    def get_fields(self):
        fields = super(CardSerializer, self).get_fields()

        active_user = self.context.get('view').request.user
        fields['categories'].child_relation.queryset = \
            CardCategory.objects.filter(owner__username=active_user)
        return fields
