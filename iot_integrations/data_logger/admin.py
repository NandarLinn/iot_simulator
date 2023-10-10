from django.contrib import admin

from .models import Hotel, Floor, Room, IoTData

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(IoTData)