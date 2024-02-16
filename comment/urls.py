from django.urls import path
from .apis import CommentCreateAPI

urlpatterns = [
    path("", CommentCreateAPI.as_view()),
]
