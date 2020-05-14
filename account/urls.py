from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from account.views import UserViewSet,regiUser,check_email,menual_token,configure_pass
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
	path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', regiUser, name='registration'),
    path('check_email/', check_email, name='check_email'),
    path('menual_token/', menual_token, name='menual_token'),
    path('configure_pass/', configure_pass, name='configure_pass'),
]