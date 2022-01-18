from rest_framework.viewsets import ModelViewSet
from .models import UserCategory, UserCard, User
from .serializers import BasicCardSerializer, BasicCardCategorySerializer, \
    CardCategoryRetrieveSerializer
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CardCategoryApi(ModelViewSet):
    queryset = UserCategory.objects.all()
    lookup_field = 'slug'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class_dict = {'list': BasicCardCategorySerializer,
                             'retrieve': CardCategoryRetrieveSerializer}

    def get_queryset(self):
        accessible_queryset = UserCategory.objects.filter(
            owner__pk=self.request.user.pk)
        return accessible_queryset

    def perform_create(self, serializer):
        auth_user_pk = User.objects.get(pk=self.request.user.pk)
        serializer.save(owner=auth_user_pk)

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action,
                                              BasicCardCategorySerializer)


class CardApi(ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = BasicCardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accessible_queryset = UserCard.objects.filter(
            categories__owner=self.request.user)
        return accessible_queryset
