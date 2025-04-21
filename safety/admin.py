from django.contrib import admin

# Register your models here.

from .models import Alert, Camera, EmergencyContact

admin.site.register(Alert)
admin.site.register(Camera)
admin.site.register(EmergencyContact)