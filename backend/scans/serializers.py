from .models import Student, Device, Event, ScanInstance, User
from rest_framework import serializers


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
        fields = ["id", "name", "homeroom", "gradYear", "email", "caassID"]


class EventSerializer(serializers.ModelSerializer):
    allowed = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Event.objects.all(),
        many=True,
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "time_start",
            "scans",
            "time_end",
            "restricted",
            "allowed",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    assigned_to = EventSerializer(read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "last_known_ip",
            "last_seen",
            "assigned_to",
            "device_type",
            "online",
        ]


class ScanInstanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = ScanInstance
        fields = ["id", "student", "time"]


class EventSerializer(serializers.ModelSerializer):
    allowed = StudentSerializer(many=True, read_only=True)
    scans = ScanInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "time_start",
            "time_end",
            "scans",
            "restricted",
            "allowed",
            "type",
        ]
