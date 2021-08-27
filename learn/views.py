from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import CardCategory, Card, User
from .serializers import CardCategorySerializer, CardSerializer, \
    CardCategoryRetrieveSerializer
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

    def get_queryset(self):
        accessible_queryset = CardCategory.objects.filter(
            owner__pk=self.request.user.pk)
        print(self.action)
        return accessible_queryset

    def perform_create(self, serializer):
        auth_user_pk = User.objects.get(pk=self.request.user.pk)
        serializer.save(owner=auth_user_pk)


class CardApi(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accessible_queryset = Card.objects.filter(
            categories__owner=self.request.user)
        return accessible_queryset
