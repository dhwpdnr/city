from rest_framework import serializers
from django.conf import settings
from .models import PlantType, Plant, PlantLog


class PlantTypeCreateSerializer(serializers.ModelSerializer):
    main_image = serializers.FileField()

    class Meta:
        model = PlantType
        fields = "__all__"


class PlantTypeReadSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = PlantType
        fields = [
            "id",
            "main_image",
            "created_at",
            "updated_at",
            "name",
            "watering_cycle",
            "repotting_cycle",
        ]

    def get_main_image(self, obj):
        return settings.MEDIA_URL + obj.main_image if obj.main_image else None


class PlantCreateSerializer(serializers.ModelSerializer):
    main_image = serializers.FileField(required=False, allow_null=True)
    nickname = serializers.CharField(allow_null=True)

    class Meta:
        model = Plant
        fields = "__all__"


class PlantReadSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    plant_type = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = "__all__"

    def get_main_image(self, obj):
        return settings.MEDIA_URL + obj.main_image if obj.main_image else None

    def get_plant_type(self, obj):
        plant_type = obj.plant_type
        if plant_type:
            return {"id": plant_type.id, "name": plant_type.name}
        return None


class MyPlantLogReadSerializer(serializers.ModelSerializer):
    plant = serializers.SerializerMethodField()

    class Meta:
        model = PlantLog
        fields = "__all__"

    def get_plant(self, obj):
        plant = obj.plant
        if plant:
            return {
                "id": plant.id,
                "main_image": settings.MEDIA_URL + plant.main_image
                if plant.main_image
                else None,
                "nickname": plant.nickname,
                "plant_type_name": plant.plant_type.name if plant.plant_type else None,
            }
        return {}


class PlantDetailSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    plant_type_name = serializers.SerializerMethodField()
    plant_type_id = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            "nickname",
            "main_image",
            "start_at",
            "plant_type_name",
            "plant_type_id",
        ]

    def get_main_image(self, obj):
        return settings.MEDIA_URL + obj.main_image if obj.main_image else None

    def get_plant_type_name(self, obj):
        return obj.plant_type.name

    def get_plant_type_id(self, obj):
        return obj.plant_type.id


class PlantLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantLog
        fields = ["type", "complete_at"]


class PlantTypeDetailSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    class Meta:
        model = PlantType
        fields = "__all__"

    def get_main_image(self, obj):
        return settings.MEDIA_URL + obj.main_image if obj.main_image else None

    def get_features(self, obj):
        features = obj.features
        if features:
            return list(features.split(","))
        return []
