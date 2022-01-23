from rest_framework.routers import SimpleRouter
from .views import UserCategoryApi, UserCardApi
from django.urls import path
from .views import (set_csrf_token, LoginApiView, LogoutApiView, LearnCardApi)

router = SimpleRouter()

router.register('dictionary', UserCategoryApi)
router.register('learn', LearnCardApi)

urlpatterns = router.urls
urlpatterns += [
    path('login/', LoginApiView.as_view(), name='url_login'),
    path('logout/', LogoutApiView.as_view(), name='url_logout'),
    path('set_csrf/', set_csrf_token, name='url_get_csrf'),
]
