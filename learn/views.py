from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import CardCategory, Card
from .serializers import CardCategorySerializer, CardSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CardCategoryApi(ModelViewSet):
    queryset = CardCategory.objects.all()
    serializer_class = CardCategorySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly]


class CardApi(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly]
