from django.urls import path
from .apis import PlanetDiaryCreateAPI, FarmDiaryCreateAPI, DiaryListAPI, DiaryDetailAPI

urlpatterns = [
    path("", DiaryListAPI.as_view()),
    path("<int:pk>", DiaryDetailAPI.as_view()),
    path("plant", PlanetDiaryCreateAPI.as_view()),
    path("farm", FarmDiaryCreateAPI.as_view()),
]
