from rest_framework import serializers
from .models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "description", "username"]

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return ""
