from rest_framework.serializers import ModelSerializer
from .models import CardCategory, Card


class CardCategorySerializer(ModelSerializer):
    class Meta:
        model = CardCategory
        fields = ['id', 'name']
