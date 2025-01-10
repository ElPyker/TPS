from rest_framework.routers import DefaultRouter
from .views import (
    TribeViewSet, UserViewSet, ItemViewSet,
    DinoViewSet, GeneticViewSet, ComboViewSet, ComboDetailViewSet
)

router = DefaultRouter()
router.register(r'tribes', TribeViewSet)
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'dinos', DinoViewSet)
router.register(r'genetics', GeneticViewSet)
router.register(r'combos', ComboViewSet)
router.register(r'combo-details', ComboDetailViewSet)

urlpatterns = router.urls
