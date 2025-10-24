from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, ScanInstance, Event, Device


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "homeroom",
            "gradYear",
            "email",
            "osis",
            "caassID",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "type",
            "time_start",
            "time_end",
            "restricted",
        ]


class ScanInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanInstance
        fields = [
            "id",
            "student",
            "event",
            "time",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "assigned_event",
            "last_known_ip",
            "last_seen",
            "device_type",
            "online",
        ]
