from rest_framework.routers import SimpleRouter
from .views import CardCategoryApi

router = SimpleRouter()

router.register('category', CardCategoryApi)

urlpatterns = router.urls
