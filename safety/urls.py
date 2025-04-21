from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, CameraViewSet, EmergencyContactViewSet, trigger_alert
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'alerts', AlertViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergencycontact')

urlpatterns = [
    path('', include(router.urls)),
    path('trigger-alert/', trigger_alert, name='trigger_alert'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
