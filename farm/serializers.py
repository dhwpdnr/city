from rest_framework import serializers
from plant.models import Plant
from django.conf import settings
from plant.models import PlantLog


class MyFarmDetailSerializer(serializers.ModelSerializer):
    plant_type_name = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    last_watered_at = serializers.SerializerMethodField()
    last_repotted_at = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            "id",
            "nickname",
            "main_image",
            "start_at",
            "plant_type_name",
            "last_watered_at",
            "last_repotted_at",
        ]

    def get_main_image(self, obj):
        return settings.MEDIA_URL + obj.main_image if obj.main_image else None

    def get_plant_type_name(self, obj):
        if obj.plant_type:
            return obj.plant_type.name
        return None

    def get_last_watered_at(self, obj):
        plant_log = (
            PlantLog.objects.filter(plant=obj, is_complete=True, type="물주기")
            .order_by("-complete_at")
            .first()
        )
        if plant_log:
            return plant_log.complete_at
        return None

    def get_last_repotted_at(self, obj):
        plant_log = (
            PlantLog.objects.filter(plant=obj, is_complete=True, type="분갈이")
            .order_by("-complete_at")
            .first()
        )
        if plant_log:
            return plant_log.complete_at
        return obj.start_at


class FarmImageUpdateSerializer(serializers.Serializer):
    farm_image = serializers.ImageField()
