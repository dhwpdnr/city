from django.urls import path
from .apis import MyFarmAPI, FarmImageUpdateAPI, UserFarmListAPI, MyFarmDetailAPI

urlpatterns = [
    path("my", MyFarmAPI.as_view()),
    path("my/<int:pk>", MyFarmDetailAPI.as_view()),
    path("image", FarmImageUpdateAPI.as_view()),
    path("target", UserFarmListAPI.as_view()),
]
