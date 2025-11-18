from django_filters import FilterSet
from .models import Student, Activity

def get_model_field_names(model):
    return [
        f.name for f in model._meta.get_fields()
    ]

class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = get_model_field_names(Student)


class ActivityFilter(FilterSet):
    class Meta:
        model = Activity
        fields = (
            get_model_field_names(Activity)
        )






