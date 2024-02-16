from rest_framework import generics, status
from rest_framework.response import Response
from .models import Diary, DiaryPlant, DairyImage
from .serializers import (
    PlanetDiaryCreateSerializer,
    FarmDiaryCreateSerializer,
    DiaryListSerializer,
    DiaryDetailSerializer,
)
from utils.authentication import IsAuthenticatedCustom


class PlanetDiaryCreateAPI(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = PlanetDiaryCreateSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"data": "참 잘했어요!"}, status=status.HTTP_201_CREATED, headers=headers
        )


class FarmDiaryCreateAPI(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = FarmDiaryCreateSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"data": "참 잘했어요!"}, status=status.HTTP_201_CREATED, headers=headers
        )


class DiaryListAPI(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type = self.request.query_params.get("type", "전체")
        location = self.request.query_params.get("location", "전체")
        plant_type = self.request.query_params.get("plant_type", "전체")

        if not type == "전체":
            queryset = queryset.filter(type=type)
        if not location == "전체":
            queryset = queryset.filter(location=location)

        if not plant_type == "전체":
            # DiaryPlant 모델을 통해 plant_type에 해당하는 Diary를 필터링합니다.
            # 이를 위해 DiaryPlant 모델에 대한 join 및 filter를 적용합니다.
            queryset = queryset.filter(
                diary_plants__plant__plant_type__name=plant_type
            ).distinct()  # 중복 제거

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})


class DiaryDetailAPI(generics.RetrieveAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryDetailSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
