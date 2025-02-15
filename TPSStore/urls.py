from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from store.views import CustomTokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # 🔹 API principal
    path('api-auth/', include('rest_framework.urls')),  # 🔹 Habilita el login en DRF
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)