from django.urls import path
from .apis import (
    PlantTypeListCreateAPI,
    PlantCreateAPI,
    MyPlantLogListAPI,
    PlantLogCompleteAPI,
    PlantDetailAPI,
    PlantTodoCompleteAPI,
    PlantTypeDetailAPI,
    PlantTagListAPI,
)

urlpatterns = [
    path("", PlantCreateAPI.as_view()),
    path("<int:pk>", PlantDetailAPI.as_view()),
    path("type", PlantTypeListCreateAPI.as_view()),
    path("tag", PlantTagListAPI.as_view()),
    path("type/<int:pk>", PlantTypeDetailAPI.as_view()),
    path("log/my", MyPlantLogListAPI.as_view()),
    path("log/complete/<int:pk>", PlantLogCompleteAPI.as_view()),
    path("todo/complete/<int:pk>", PlantTodoCompleteAPI.as_view()),
]
