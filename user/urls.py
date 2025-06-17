from django.urls import path
from .views import RegisterAPIView,LoginAPIView,UserActivityLogListCreateAPIView,UserActivityLogTransitionAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/register', RegisterAPIView.as_view(), name='user/register'),
    path('user/login', LoginAPIView.as_view(), name='user/login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/activity', UserActivityLogListCreateAPIView.as_view(), name='user/activity'),
    path('user/activityupdate', RegisterAPIView.as_view(), name='user/activityupdate')
]