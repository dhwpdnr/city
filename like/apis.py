from rest_framework.generics import GenericAPIView
from .serializers import LikeDiarySerializer
from rest_framework.response import Response
from rest_framework import status
from utils.authentication import IsAuthenticatedCustom
from diary.models import Diary
from .models import Like


class LikeDiaryAPI(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeDiarySerializer
    permission_classes = (IsAuthenticatedCustom,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        diary = request.data.get("diary", None)
        like_count = 0
        if diary:
            like_count = Like.objects.filter(diary_id=diary).count()
        return Response(
            status=status.HTTP_200_OK,
            data={"like_count": like_count, "is_like": True if instance else False},
        )
