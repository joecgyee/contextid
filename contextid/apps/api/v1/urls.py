from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .accounts.views import RegisterView, UserMeView
from .contexts.views import ContextViewSet
from .profiles.views import ProfileViewSet
from .core.views import IdentityResolutionView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'contexts', ContextViewSet, basename='context')
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/me/', UserMeView.as_view(), name='user_me'),

    # Register all automatically generated routes from the router at the root URL
    path('', include(router.urls)),

    # Core Feature
    path('identity/', IdentityResolutionView.as_view(), name='identity_resolution'),
    
    # Schema & Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='api:v1:schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='api:v1:schema'), name='redoc'),
]