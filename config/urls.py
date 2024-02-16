from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("plant/", include("plant.urls")),
    path("farm/", include("farm.urls")),
    path("diary/", include("diary.urls")),
    path("like/", include("like.urls")),
    path("comment", include("comment.urls")),
]
