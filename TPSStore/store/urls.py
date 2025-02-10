from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TribeViewSet, UserViewSet, ItemViewSet, DinoViewSet, GeneticViewSet, 
    ComboViewSet, ComboDetailViewSet, AccountViewSet, 
    SessionViewSet, SessionLogViewSet, CustomTokenObtainPairView, get_current_user
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tribes', TribeViewSet)
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'dinos', DinoViewSet)
router.register(r'genetics', GeneticViewSet)
router.register(r'combos', ComboViewSet)
router.register(r'combo-details', ComboDetailViewSet)
router.register(r'accounts', AccountViewSet)  # Nueva ruta para cuentas de Steam
router.register(r'sessions', SessionViewSet)  # Nueva ruta para sesiones activas
router.register(r'session-logs', SessionLogViewSet)  # Nueva ruta para historial de sesiones


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', get_current_user, name='current_user'),
]

urlpatterns += router.urls