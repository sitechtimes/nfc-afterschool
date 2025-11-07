from django.conf import settings
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from .filters import *
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

# according to ben, the only user is an admin so normal is authenticatde should be fine

BASE_URL = settings.NFC_BASE_URL


def fetch_remote(endpoint):
    url = f"{settings.REMOTE_BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class BaseSyncView(APIView):
    permission_classes = [IsAuthenticated]
    model = None
    fetch_url = None
    related_fields = {}

    def syncData(self, request):
        if not self.model or not self.fetch_url:
            return Response(
                {"status": "error", "message": "Model or fetch_url not defined"},
                status=400,
            )

        try:
            data_list = fetch_remote(self.fetch_url)

            for data in data_list:
                for field, related_model in self.related_fields.items():
                    related_id = data.pop(f"{field}_id", None)

                    try:
                        data[field] = related_model.objects.get(id=related_id)
                    except related_model.DoesNotExist:
                        raise Exception(
                            f"Related {related_model.__name__} with id {related_id} does not exist"
                        )

                self.model.objects.update_or_create(id=data["id"], defaults=data)

            return Response(
                {"status": "success", "message": f"{self.model.__name__} synchronized"},
                status=200,
            )

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


class UserViewSet(
    viewsets.ModelViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet, BaseSyncView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    model = Student
    fetch_url = "students/list/"

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)


class EventViewSet(viewsets.ModelViewSet):
    # not base because m2m im not doing allat
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def sync(self, request):
        try:
            data_list = fetch_remote("events/list/")
            for data in data_list:
                microservice_id = data.pop("MicroService_id", None)
                try:
                    data["MicroService"] = MicroService.objects.get(id=microservice_id)
                except MicroService.DoesNotExist:
                    raise Exception(
                        f"Related MicroService with id {microservice_id} does not exist"
                    )

                allowed_ids = data.pop("allowed_ids", [])
                scan_ids = data.pop("scan_ids", [])

                event, created = Event.objects.update_or_create(
                    id=data["id"], defaults=data
                )
                if allowed_ids:
                    event.allowed.set(Student.objects.filter(id__in=allowed_ids))
                if scan_ids:
                    event.scans.set(ScanInstance.objects.filter(id__in=scan_ids))

            return Response(
                {"status": "success", "message": "Events synchronized"}, status=200
            )

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


class DeviceViewSet(BaseSyncView, viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_class = DeviceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    model = Device
    fetch_url = "devices/list/"
    related_fields = {"assigned_to": Event}

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)


class ScanInstanceViewSet(BaseSyncView, viewsets.ModelViewSet):
    queryset = ScanInstance.objects.all()
    serializer_class = ScanInstanceSerializer
    filterset_class = ScanInstanceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    model = ScanInstance
    fetch_url = "connect/list/scans/"
    related_fields = {"event": Event, "student": Student}

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)
