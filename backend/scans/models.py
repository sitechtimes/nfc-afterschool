from django.db import models
import uuid

#ill keep this as is for now cuz thats what you said in the pr
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

#ben said he wants to change the name to activity
class Activity(models.Model):
    nfc_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"






