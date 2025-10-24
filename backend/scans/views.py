from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from .filters import *


class BaseModelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [
        IsAuthenticated
    ]  # according to ben, the only user is an admin so normal is authenticatde should be fine


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentViewSet(BaseModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter


class EventViewSet(BaseModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter


class DeviceViewSet(BaseModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_class = DeviceFilter


class ScanInstanceViewSet(BaseModelViewSet):
    queryset = ScanInstance.objects.all()
    serializer_class = ScanInstanceSerializer
    filterset_class = ScanInstanceFilter
