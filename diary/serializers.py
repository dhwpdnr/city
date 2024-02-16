from rest_framework import serializers
from .models import Diary, DairyImage, DiaryPlant
from utils.media import save_media
from plant.models import Plant
from like.models import Like
from comment.models import Comment
from comment.serializers import CommentListSerializer
from django.conf import settings


class PlanetDiaryCreateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False, allow_null=True)
    plants = serializers.ListSerializer(
        child=serializers.IntegerField(required=False), required=False
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), write_only=True
    )

    class Meta:
        model = Diary
        fields = ["user", "title", "location", "description", "plants", "image"]

    def create(self, validated_data):
        plants = validated_data.pop("plants", [])
        image = validated_data.pop("image", None)
        validated_data["type"] = "농업일지"
        diary = Diary.objects.create(**validated_data)
        if image:
            file_path, original_name = save_media(image, "diary_plants")
            DairyImage.objects.create(diary=diary, path=file_path)
        if plants:
            for plant in plants:
                diary_plant = DiaryPlant.objects.create(plant_id=plant, diary=diary)
                diary_plant.save()

        return diary


class FarmDiaryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), write_only=True
    )

    class Meta:
        model = Diary
        fields = ["user", "title", "location", "description"]

    def create(self, validated_data):
        user = validated_data.get("user")
        validated_data["farm_image"] = user.farm_image
        plants = Plant.objects.filter(user=user).all()
        validated_data["type"] = "밭자랑"
        diary = Diary.objects.create(**validated_data)
        for plant in plants:
            diary_plant = DiaryPlant.objects.create(plant=plant, diary=diary)
            diary_plant.save()
        return diary


class DiaryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = [
            "id",
            "title",
            "description",
            "type",
            "location",
            "user",
            "image",
            "tags",
            "like_count",
            "comment_count",
            "created_at",
        ]

    def get_image(self, obj):
        type = obj.type
        if type == "농업일지":
            diary_image = DairyImage.objects.filter(diary=obj)
            if diary_image:
                return settings.MEDIA_URL + diary_image.first().path
            return ""
        return settings.MEDIA_URL + obj.farm_image

    def get_tags(self, obj):
        plant_type_names = (
            obj.diary_plants.all()
            .values_list("plant__plant_type__name", flat=True)
            .distinct()
        )
        plant_type_names_list = list(plant_type_names)
        plant_type_names_list.append(obj.location)

        return plant_type_names_list

    def get_like_count(self, obj):
        return Like.objects.filter(diary=obj).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(diary=obj).count()

    def get_created_at(self, obj):
        created_at = obj.created_at
        return created_at.strftime("%Y-%m-%d")


class DiaryDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    my_farm_item_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    tagged_item_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = [
            "id",
            "type",
            "title",
            "description",
            "tags",
            "image",
            "username",
            "user_id",
            "my_farm_item_count",
            "like_count",
            "comment_count",
            "tagged_item_count",
            "comments",
            "is_liked",
        ]

    def get_tags(self, obj):
        plant_type_names = (
            obj.diary_plants.all()
            .values_list("plant__plant_type__name", flat=True)
            .distinct()
        )
        plant_type_names_list = list(plant_type_names)
        plant_type_names_list.append(obj.location)

        return plant_type_names_list

    def get_image(self, obj):
        type = obj.type
        if type == "농업일지":
            diary_image = DairyImage.objects.filter(diary=obj)
            if diary_image:
                return settings.MEDIA_URL + diary_image.first().path
            return ""
        return settings.MEDIA_URL + obj.farm_image

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return ""

    def get_user_id(self, obj):
        if obj.user:
            return obj.user.id
        return ""

    def get_my_farm_item_count(self, obj):
        if obj.user:
            return obj.user.plants.count()
        return 0

    def get_like_count(self, obj):
        return Like.objects.filter(diary=obj).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(diary=obj).count()

    def get_tagged_item_count(self, obj):
        return obj.diary_plants.all().count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(diary=obj).all()
        return CommentListSerializer(comments, many=True).data

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user or user.is_anonymous:
            return False
        return Like.objects.filter(user=user, diary=obj).exists()
