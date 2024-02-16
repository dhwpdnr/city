from .models import Plant, PlantLog
from datetime import timedelta


def create_plant_log(plant, type, deadline):
    PlantLog.objects.create(plant=plant, type=type, deadline=deadline)
