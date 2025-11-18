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


# this is under the assumption that im fetching from nfc and you're not sending data to us
def fetch_remote(endpoint):
    url = f"{settings.REMOTE_BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class AttendenceView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            data = fetch_remote("scan-instances/list/")
            filtered_data = [
                entry for entry in data if entry.get("event_type") == "afterschool"
            ]
            return Response(filtered_data, status=200)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


# ben said he wanted a wya to mually make these things as well


class CreateScan(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        payload = request.data
        url = f"{settings.NFC_BASE_URL}scan-instances/create/"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return Response(response.json())
        except requests.HTTPError as e:
            return Response({"error": str(e)}, status=e.response.status_code)


class CreateActivity(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        payload = {
            "name": request.data.get("name"),
            "time_start": request.data.get("time_start"),
            "time_end": request.data.get("time_end"),
            "type": "afterschool",
        }
        url = f"{BASE_URL}events/create/"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return Response(response.json())
        except requests.HTTPError as e:
            return Response({"error": str(e)}, status=e.response.status_code)


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


class ActivityViewSet(BaseSyncView, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filterset_class = ActivityFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAdminUser]
    model = Activity
    fetch_url = "events/list/"

    @action(detail=False, methods=["post"])
    def sync(self, request):
        return self.syncData(request)
