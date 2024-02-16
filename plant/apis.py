from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    PlantTypeCreateSerializer,
    PlantTypeReadSerializer,
    PlantCreateSerializer,
    PlantReadSerializer,
    MyPlantLogReadSerializer,
    PlantDetailSerializer,
    PlantLogListSerializer,
    PlantTypeDetailSerializer,
)
from farm.serializers import MyFarmDetailSerializer
from .models import PlantType, Plant, PlantLog
from diary.models import DiaryPlant
from django.db import transaction
from utils.media import save_media
from utils.authentication import IsAuthenticatedCustom
from utils.exceptions import CustomValidationError
from datetime import datetime, timedelta, date
from .utils import create_plant_log


class PlantTypeListCreateAPI(generics.ListCreateAPIView):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeCreateSerializer
    read_serializer = PlantTypeReadSerializer

    def perform_create(self, serializer):
        return serializer.save()

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        main_image = serializer.validated_data.get("main_image", None)
        if main_image:
            file_path, original_name = save_media(main_image, "plant_types")
            instance.main_image = file_path
            instance.save()
        data = self.read_serializer(instance).data
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.read_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.read_serializer(queryset, many=True)
        return Response(serializer.data)


class PlantCreateAPI(generics.CreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantCreateSerializer
    read_serializer = PlantReadSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        main_image = serializer.validated_data.get("main_image", None)
        plant = serializer.save(user=request.user)
        if main_image:
            file_path, original_name = save_media(main_image, "plants")
            plant.main_image = file_path
        if not plant.nickname:
            plant.nickname = plant.plant_type.name
        plant.save()
        plant_type = plant.plant_type

        last_watered_at = request.data.get("watered_at")
        last_watered_at = datetime.strptime(last_watered_at, "%Y-%m-%d").date()
        last_repotted_at = request.data.get("repotted_at")
        last_repotted_at = datetime.strptime(last_repotted_at, "%Y-%m-%d").date()

        PlantLog.objects.create(
            plant=plant,
            type="시작",
            deadline=plant.start_at,
            complete_at=plant.start_at,
            is_complete=True,
        )
        PlantLog.objects.create(
            plant=plant,
            type="물주기",
            deadline=last_watered_at,
            complete_at=last_watered_at,
            is_complete=True,
        )
        if not last_repotted_at == plant.start_at:
            PlantLog.objects.create(
                plant=plant,
                type="분갈이",
                deadline=last_repotted_at,
                complete_at=last_repotted_at,
                is_complete=True,
            )

        watering_log = create_plant_log(
            plant, "물주기", last_watered_at + timedelta(days=plant_type.watering_cycle)
        )
        repot_log = create_plant_log(
            plant, "분갈이", last_repotted_at + timedelta(days=plant_type.repotting_cycle)
        )

        serializer = self.read_serializer(plant)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MyPlantLogListAPI(generics.GenericAPIView):
    queryset = PlantLog.objects.all()
    permission_classes = (IsAuthenticatedCustom,)

    def get_queryset(self):
        return self.queryset.filter(plant__user=self.request.user)

    def serializered_data(self, data):
        return MyPlantLogReadSerializer(data, many=True).data

    def get(self, request):
        queryset = self.get_queryset()
        watering_query = queryset.filter(
            type="물주기", is_complete=False, deadline__lte=date.today()
        )
        repotting_query = queryset.filter(
            type="분갈이", is_complete=False, deadline__lte=date.today()
        )
        watering_complete_query = queryset.filter(
            type="물주기", is_complete=True, complete_at=date.today()
        )
        repotting_complete_query = queryset.filter(
            type="분갈이", is_complete=True, complete_at=date.today()
        )
        data = {"data": []}
        if watering_query.exists():
            data["data"].append(
                {"type": "watering", "tasks": self.serializered_data(watering_query)}
            )
        if repotting_query.exists():
            data["data"].append(
                {"type": "repotting", "tasks": self.serializered_data(repotting_query)}
            )
        if watering_complete_query.exists():
            data["data"].append(
                {
                    "type": "watering_complete",
                    "tasks": self.serializered_data(watering_complete_query),
                }
            )
        if repotting_complete_query.exists():
            data["data"].append(
                {
                    "type": "repotting_complete",
                    "tasks": self.serializered_data(repotting_complete_query),
                }
            )

        return Response(data=data, status=status.HTTP_200_OK)


class PlantLogCompleteAPI(generics.UpdateAPIView):
    queryset = PlantLog.objects.all()
    permission_classes = (IsAuthenticatedCustom,)

    def get_queryset(self):
        return self.queryset.filter(plant__user=self.request.user)

    def serializered_data(self, data):
        return MyPlantLogReadSerializer(data, many=True).data

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if not instance.plant.user == user:
            raise CustomValidationError({"data": "본인의 작물만 완료처리 할 수 있습니다."})

        if instance.is_complete:
            raise CustomValidationError({"data": "이미 완료 상태 입니다."})

        plant = instance.plant
        type = instance.type
        cycle = (
            plant.plant_type.watering_cycle
            if instance.type == "물주기"
            else plant.plant_type.repotting_cycle
        )
        instance.is_complete = True
        instance.save()

        new_log = create_plant_log(plant, type, datetime.now() + timedelta(days=cycle))

        queryset = self.get_queryset()
        watering_query = queryset.filter(
            type="물주기", is_complete=False, deadline__lte=date.today()
        )
        repotting_query = queryset.filter(
            type="분갈이", is_complete=False, deadline__lte=date.today()
        )
        watering_complete_query = queryset.filter(
            type="물주기", is_complete=True, complete_at=date.today()
        )
        repotting_complete_query = queryset.filter(
            type="분갈이", is_complete=True, complete_at=date.today()
        )
        data = {"data": []}
        if watering_query.exists():
            data["data"].append(
                {"type": "watering", "tasks": self.serializered_data(watering_query)}
            )
        if repotting_query.exists():
            data["data"].append(
                {"type": "repotting", "tasks": self.serializered_data(repotting_query)}
            )
        if watering_complete_query.exists():
            data["data"].append(
                {
                    "type": "watering_complete",
                    "tasks": self.serializered_data(watering_complete_query),
                }
            )
        if repotting_complete_query.exists():
            data["data"].append(
                {
                    "type": "repotting_complete",
                    "tasks": self.serializered_data(repotting_complete_query),
                }
            )
        return Response(data=data, status=status.HTTP_200_OK)


class PlantDetailAPI(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        queryset = PlantLog.objects.filter(plant=instance).all()
        not_complete_query = queryset.filter(
            is_complete=False, deadline__lte=date.today()
        )
        complete_query = queryset.filter(is_complete=True, complete_at=date.today())
        combined_query = not_complete_query | complete_query

        combined_data = MyPlantLogReadSerializer(combined_query, many=True).data

        data["todos"] = combined_data

        record_query = (
            PlantLog.objects.filter(plant=instance, is_complete=True)
            .all()
            .order_by("-complete_at")
        )
        record_data = PlantLogListSerializer(record_query, many=True).data
        data["records"] = record_data
        return Response(data)


class PlantTodoCompleteAPI(generics.UpdateAPIView):
    queryset = PlantLog.objects.all()
    permission_classes = (IsAuthenticatedCustom,)

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if not instance.plant.user == user:
            raise CustomValidationError({"data": "본인의 작물만 완료처리 할 수 있습니다."})
        plant = instance.plant
        type = instance.type
        cycle = (
            plant.plant_type.watering_cycle
            if instance.type == "물주기"
            else plant.plant_type.repotting_cycle
        )
        instance.is_complete = True
        instance.save()

        new_log = create_plant_log(plant, type, datetime.now() + timedelta(days=cycle))

        return Response({"data": "complete !! ^^"})


class PlantTypeDetailAPI(generics.RetrieveAPIView):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeDetailSerializer


class PlantTagListAPI(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = MyFarmDetailSerializer

    def get_queryset(self):
        queryset = self.queryset
        diary_id = self.request.query_params.get("diary", None)
        if not diary_id:
            raise CustomValidationError({"data": "일지 정보가 없습니다."})
        queryset = queryset.filter(diary_plants__diary_id=diary_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
