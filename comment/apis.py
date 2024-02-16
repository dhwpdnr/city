from rest_framework import generics, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer
from utils.authentication import IsAuthenticatedCustom


class CommentCreateAPI(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        diary = comment.diary
        comments = diary.comments.all().order_by("created_at")
        serializer = CommentListSerializer(comments, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers
        )
