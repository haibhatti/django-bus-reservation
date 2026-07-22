from django.contrib import admin
from .models import Location, Bus, Trip, FareMatrix, Ticket

# Register your models here.

admin.site.register(Location)
admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(FareMatrix)
admin.site.register(Ticket)