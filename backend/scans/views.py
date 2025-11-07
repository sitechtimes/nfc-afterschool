from django.conf import settings
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from .filters import *
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action


BASE_URL = settings.NFC_BASE_URL


def fetch_remote(endpoint):
    url = f"{settings.REMOTE_BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class BaseSyncView(APIView):
    permission_classes = [IsAdminUser]
    model = None
    serializer_class = None
    fetch_url = None

    def syncData(self, request):
        if not self.model or not self.fetch_url or not self.serializer_class:
            return Response(
                {
                    "status": "error",
                    "message": "model, serializer_class, or fetch_url missing",
                },
                status=400,
            )

        try:
            data = fetch_remote(self.fetch_url)

            for item in data:
                instance = None
                obj_id = item.get("id")

                if obj_id:
                    try:
                        instance = self.model.objects.get(id=obj_id)
                    except self.model.DoesNotExist:
                        instance = None  

                serializer = self.serializer_class(instance=instance, data=item)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response({"status": "success"}, status=200)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


class UserViewSet(
    viewsets.ModelViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet, BaseSyncView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]
    model = Student
    fetch_url = "students/list/"

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)


class EventViewSet(BaseSyncView,viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)


class DeviceViewSet(BaseSyncView, viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_class = DeviceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]
    model = Device
    fetch_url = "devices/list/"

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)


class ScanInstanceViewSet(BaseSyncView, viewsets.ModelViewSet):
    queryset = ScanInstance.objects.all()
    serializer_class = ScanInstanceSerializer
    filterset_class = ScanInstanceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]
    model = ScanInstance
    fetch_url = "connect/list/scans/"

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)
