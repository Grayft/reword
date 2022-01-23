from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import UserCategory, UserCard, User, BasicCategory
from .serializers import (UserCardSerializer, BaseUserCategorySerializer,
                          UserCategoryRetrieveSerializer,
                          LoginRequestSerializer)
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from django.http import JsonResponse


class UserCategoryApi(ModelViewSet):
    queryset = UserCategory.objects.all()
    lookup_field = 'slug'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]
    serializer_class_dict = {'list': BaseUserCategorySerializer,
                             'retrieve': UserCategoryRetrieveSerializer}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            accessible_queryset = UserCategory.objects.filter(
                owner__pk=self.request.user.pk)
            return accessible_queryset
        else:
            basic_category_queryset = BasicCategory.objects.all()
            return basic_category_queryset

    def perform_create(self, serializer):
        auth_user_pk = User.objects.get(pk=self.request.user.pk)
        serializer.save(owner=auth_user_pk)

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action,
                                              BaseUserCategorySerializer)


class UserCardApi(ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accessible_queryset = UserCard.objects.filter(
            categories__owner=self.request.user)
        return accessible_queryset


class LearnCardApi(ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        learning_cards = UserCard.objects.filter(owner=self.request.user,
                                                 categories__is_selected=True,
                                                 status='New word')
        return learning_cards

@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})


class LoginApiView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginRequestSerializer(data=self.request.data)
        if serializer.is_valid():
            authenticated_user = authenticate(**serializer.validated_data)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return Response({'status': 'Success'
                                 })
            else:
                return Response({'error': 'Invalid credentials'}, status=403)
        else:
            return Response(serializer.errors, status=400)


class LogoutApiView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'Success'})

# {
#     "username": "admin",
#     "password": "admin"
# }
