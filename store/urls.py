from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TribeViewSet, UserViewSet, ItemViewSet, DinoViewSet, GeneticViewSet, 
    ComboViewSet, ComboDetailViewSet, AccountViewSet, 
    SessionViewSet, SessionLogViewSet, CustomTokenObtainPairView, RecipeViewSet, RecipeIngredientViewSet, BlueprintViewSet, BlueprintMaterialViewSet, SalePostViewSet, get_current_user
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
router = DefaultRouter()
router.register(r'tribes', TribeViewSet)
router.register(r'users', UserViewSet)
router.register(r'dinos', DinoViewSet)
router.register(r'genetics', GeneticViewSet)
router.register(r'combos', ComboViewSet)
router.register(r'combo-details', ComboDetailViewSet)
router.register(r'accounts', AccountViewSet)  # Nueva ruta para cuentas de Steam
router.register(r'sessions', SessionViewSet)  # Nueva ruta para sesiones activas
router.register(r'session-logs', SessionLogViewSet)  # Nueva ruta para historial de sesiones
router.register(r'items', ItemViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)
router.register(r'blueprints', BlueprintViewSet)
router.register(r'blueprint-materials', BlueprintMaterialViewSet)
router.register(r'salepost', SalePostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', get_current_user, name='current_user'),
]

urlpatterns += router.urls