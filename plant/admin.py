from django.contrib import admin
from .models import Plant, PlantType, PlantLog


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantLog)
class PlantLogAdmin(admin.ModelAdmin):
    pass
