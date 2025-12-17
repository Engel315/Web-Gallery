from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/", views.gallery_view, name="gallery_root"),
    path("gallery/<path:folder>/", views.gallery_view, name="gallery_folder"),
    path("photos/json/", views.photos_json, name="photos_json"),
]
