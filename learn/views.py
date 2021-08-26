from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import CardCategory, Card, User
from .serializers import CardCategorySerializer, CardSerializer
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated


class CardCategoryApi(ModelViewSet):
    queryset = CardCategory.objects.all()
    serializer_class = CardCategorySerializer
    lookup_field = 'slug'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        creating_user = User.objects.get(username=self.request.user)
        serializer.save(owner=creating_user)

    def get_queryset(self):
        accessible_queryset = CardCategory.objects.filter(
            owner__username=self.request.user)
        return accessible_queryset


class CardApi(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        accessible_queryset = Card.objects.filter(
            categories__owner=self.request.user)
        return accessible_queryset