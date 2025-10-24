from django_filters import FilterSet
from .models import Student, Event, Device, ScanInstance, MicroService


def get_model_field_names(model):
    return [
        f.name for f in model._meta.get_fields() if not f.is_relation or f.many_to_one
    ]


def get_related_fields(
    prefix,
    model,
):
    fields = []
    for f in model._meta.get_fields():
        fields.append(f"{prefix}__{f.name}")
    return fields


class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = get_model_field_names(Student)


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = (
            get_model_field_names(Event)
            + get_related_fields("MicroService", MicroService)
            + get_related_fields("allowed", Student)
            + get_related_fields("scans", ScanInstance)
        )


class DeviceFilter(FilterSet):
    class Meta:
        model = Device
        fields = (
            get_model_field_names(Device)
            + get_related_fields("assigned_to", Event)
            + get_related_fields("assigned_to__MicroService", MicroService)
        )


class ScanInstanceFilter(FilterSet):
    class Meta:
        model = ScanInstance
        fields = (
            get_model_field_names(ScanInstance)
            + get_related_fields("student", Student)
            + get_related_fields("event", Event)
            + get_related_fields("event__MicroService", MicroService)
        )
