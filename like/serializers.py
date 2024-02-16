from rest_framework import serializers
from .models import Like


class LikeDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "diary"]
        extra_kwargs = {"user": {"read_only": True}}

    def save(self, **kwargs):
        # 현재 요청한 사용자를 user 필드로 설정
        user = self.context["request"].user
        diary = self.validated_data["diary"]

        # Like 인스턴스 검색
        like_instance, created = Like.objects.get_or_create(
            user=user, diary=diary, defaults={"user": user, "diary": diary}
        )

        if not created:
            # Like 인스턴스가 이미 존재하면, 해당 인스턴스 삭제
            like_instance.delete()
            return None
        # 새로운 Like 인스턴스가 생성되었다면 반환
        return like_instance


#
# class LikeDiarySerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = Like
#         fields = "__all__"
#
#     def save(self, *args, **kwargs):
#         like = Like.objects.filter(
#             user=self.context["request"].user,
#             diary=self.validated_data["diary"],
#         ).first()
#         print(like)
#         if like:
#             like.delete()
#             return None
#         else:
#             return super().save(*args, **kwargs)
