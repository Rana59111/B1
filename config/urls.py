# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from safety.views import AlertViewSet, CameraViewSet, EmergencyContactViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView

router = DefaultRouter()
router.register(r'alerts', AlertViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergencycontact')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
]
