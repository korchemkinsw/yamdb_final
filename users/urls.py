from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenObtainPairView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users')

extra_patterns = [
    path('auth/email/', SignUpView.as_view(), name='auth_email'),
    path('auth/token/', TokenObtainPairView.as_view(), name='auth_token'),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(extra_patterns)),
]
