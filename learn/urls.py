from rest_framework.routers import SimpleRouter
from .views import CardCategoryApi, CardApi

router = SimpleRouter()

router.register('category', CardCategoryApi)
router.register('card', CardApi)

urlpatterns = router.urls
