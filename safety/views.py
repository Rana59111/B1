# safety/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Alert, Camera, EmergencyContact
from .serializers import AlertSerializer, CameraSerializer, EmergencyContactSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Alert, Camera
from django.contrib.auth.models import User

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-timestamp')
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self):
        active_alerts = Alert.objects.filter(is_active=True)
        serializer = self.get_serializer(active_alerts, many=True)
        return Response(serializer.data)

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active(self):
        active_cameras = Camera.objects.filter(is_active=True)
        serializer = self.get_serializer(active_cameras, many=True)
        return Response(serializer.data)

class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])  # Later change this to Token Auth
def trigger_alert(request):
    """
    Accepts data from camera AI system to create an alert.
    """
    try:
        camera_id = request.data.get('camera_id')
        description = request.data.get('description', 'Suspicious activity detected')
        severity = request.data.get('severity', 'critical')

        camera = Camera.objects.get(id=camera_id)
        default_user = User.objects.first()  # Replace with real system user in future

        alert = Alert.objects.create(
            title="Automated Alert",
            description=description,
            location=camera.location,
            severity=severity,
            created_by=default_user
        )

        # Set camera flag
        camera.has_alert = True
        camera.save()

        return Response({"status": "success", "alert_id": alert.id}, status=201)

    except Camera.DoesNotExist:
        return Response({"error": "Invalid camera ID"}, status=400)