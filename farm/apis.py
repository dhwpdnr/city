from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from plant.models import Plant
from .serializers import MyFarmDetailSerializer, FarmImageUpdateSerializer
from utils.authentication import IsAuthenticatedCustom
from utils.exceptions import CustomValidationError
from utils.media import save_media
from django.conf import settings
from users.models import User


class MyFarmAPI(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = MyFarmDetailSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        return queryset.filter(user=user).all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_data = self.get_serializer(queryset, many=True).data
        data = {"farm_image": request.user.farm_image, "plants": serializer_data}
        return Response(data)


class MyFarmDetailAPI(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = MyFarmDetailSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        return queryset.filter(user=user).all()

    def list(self, request, *args, **kwargs):
        selected_plant = self.get_object()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data

        for plant_data in serializer_data:
            plant_data["is_selected"] = str(plant_data["id"]) == str(selected_plant.id)

        data = {"farm_image": request.user.farm_image, "plants": serializer_data}
        return Response(data)


class FarmImageUpdateAPI(generics.GenericAPIView):
    serializer_class = FarmImageUpdateSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        farm_image = serializer.validated_data.get("farm_image", None)
        if farm_image:
            file_path, original_name = save_media(farm_image, "farms")
            user.farm_image = settings.MEDIA_URL + file_path
            user.save()
        return Response({"data": "success"})


class UserFarmListAPI(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = MyFarmDetailSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user", None)
        if not user_id:
            raise CustomValidationError({"data": "유저 정보를 보내야합니다"})
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise CustomValidationError({"data": "유저 정보가 없습니다"})
        return queryset.filter(user=user).all()

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user", None)
        if not user_id:
            raise CustomValidationError({"data": "유저 정보를 보내야합니다"})
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise CustomValidationError({"data": "유저 정보가 없습니다"})
        print(user)
        queryset = self.filter_queryset(self.get_queryset())
        serializer_data = self.get_serializer(queryset, many=True).data
        data = {
            "farm_image": user.farm_image,
            "plants": serializer_data,
            "username": user.username,
        }
        return Response(data)
