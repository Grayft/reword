from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import CardCategory
from .serializers import CardCategorySerializer


class CardCategoryApi(ReadOnlyModelViewSet):
    queryset = CardCategory.objects.all()
    serializer_class = CardCategorySerializer
