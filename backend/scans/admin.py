from django.contrib import admin
from .models import Student, ScanInstance, Event, Device, MicroService

# Register your models here.
admin.site.register(Student)
admin.site.register(ScanInstance)
admin.site.register(Event)
admin.site.register(Device)
admin.site.register(MicroService)
