from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    RefreshSerializer,
    UserSerializer,
    CheckUsernameSerializer,
)
from .models import User, Jwt
from .utils import get_access_token, get_refresh_token
from .authentication import Authentication
from utils.authentication import IsAuthenticatedCustom
from django.db import transaction
from django.contrib.auth import authenticate
from plant.models import Plant, PlantType, PlantLog
from plant.utils import create_plant_log
from utils.dummy import plants_data
from datetime import timedelta, datetime


class SignupAPI(APIView):
    serializer_class = SignupSerializer

    @transaction.atomic()
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("password2")
        user = User.objects._create_user(**serializer.validated_data)
        for data in plants_data:
            plant_type = PlantType.objects.filter(name=data["type"]).first()
            if not plant_type:
                continue
            plant = Plant.objects.create(
                nickname=data["nickname"],
                plant_type=plant_type,
                start_at=data["start_at"],
                user=user,
                main_image=plant_type.main_image,
            )
            plant.save()

            last_watered_at = data["last_watered_at"]
            last_watered_at = datetime.strptime(last_watered_at, "%Y-%m-%d").date()
            last_repotted_at = data["last_repotted_at"]
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
                plant,
                "물주기",
                last_watered_at + timedelta(days=plant_type.watering_cycle),
            )
            repot_log = create_plant_log(
                plant,
                "분갈이",
                last_repotted_at + timedelta(days=plant_type.repotting_cycle),
            )

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response({"error": "등록된 유저가 아닙니다"}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id=user.id,
            access=access,
            refresh=refresh,
        )

        return Response(
            status=status.HTTP_200_OK,
            data={"username": user.username, "access": access, "refresh": refresh},
        )


class RefreshAPI(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"data": "존재하지 않는 토큰입니다."}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"data": "토큰이 만료되었습니다."})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})


class LogoutAPI(APIView):
    permission_classes = (IsAuthenticatedCustom,)

    def post(self, request):
        user_id = request.user.id

        Jwt.objects.filter(user_id=user_id).delete()

        request.session.flush()

        return Response("logged out successfully", status=200)


class CheckUsernameAPI(generics.GenericAPIView):
    serializer_class = CheckUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"data": "사용 가능한 닉네임 입니다."}, status=200)
