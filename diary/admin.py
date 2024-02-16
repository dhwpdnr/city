from django.contrib import admin
from .models import Diary, DairyImage, DiaryPlant


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass


@admin.register(DairyImage)
class DairyImageAdmin(admin.ModelAdmin):
    pass


@admin.register(DiaryPlant)
class DiaryPlantAdmin(admin.ModelAdmin):
    pass
