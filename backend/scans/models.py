from django.db import models
import uuid


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    homeroom = models.CharField(max_length=4)
    gradYear = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    osis = models.CharField(max_length=9, null=True, blank=True)
    caassID = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class ScanInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.DateTimeField()
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} "


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    scans = models.ManyToManyField(
        ScanInstance, blank=True, related_name="event_scanned"
    )
    restricted = models.BooleanField(default=False)
    allowed = models.ManyToManyField(Student, blank=True)
    MicroServiceEnabled = models.BooleanField(default=False)
    MicroService = models.ForeignKey(
        "MicroService", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    last_known_ip = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    device_type = models.CharField(max_length=10, null=True, blank=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"


class MicroService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.url})"
