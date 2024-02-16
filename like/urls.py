from django.urls import path
from .apis import LikeDiaryAPI

urlpatterns = [
    path("", LikeDiaryAPI.as_view()),
]
