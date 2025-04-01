from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Rota do admin
    path('admin/', admin.site.urls),

    # Rotas específicas do app de equipamentos
    path('api/', include('equipamentos.urls')),

    # Endpoints para autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
