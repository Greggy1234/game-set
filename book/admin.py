from django.contrib import admin
from .models import Location, Court, CourtAvailability, Coach, CoachAvailability

# Register your models here.
admin.site.register(Location),
admin.site.register(Court),
admin.site.register(CourtAvailability),
admin.site.register(Coach),
admin.site.register(CoachAvailability),