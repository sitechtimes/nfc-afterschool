from django.conf import settings
from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from .filters import *
import requests
from rest_framework import viewsets
from .filters import get_model_field_names,get_related_fields

# according to ben, the only user is an admin so normal is authenticatde should be fine


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_class = DeviceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


class ScanInstanceViewSet(viewsets.ModelViewSet):
    queryset = ScanInstance.objects.all()
    serializer_class = ScanInstanceSerializer
    filterset_class = ScanInstanceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


BASE_URL = settings.NFC_BASE_URL
NFC_USERNAME = settings.NFC_USERNAME
NFC_PASSWORD = settings.NFC_PASSWORD


def fetch_remote(endpoint):
    url = f"{settings.REMOTE_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Api-Key {settings.REMOTE_API_KEY}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_all_remote_data():
    return {
        "events": fetch_remote("events/list/"),
        "devices": fetch_remote("devices/list/"),
        "students": fetch_remote("students/list/"),
        "scans": fetch_remote("connect/list/scans/"),
        "microservices": fetch_remote("connect/list/microservices/"),
    }


