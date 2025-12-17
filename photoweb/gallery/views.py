from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from .utils import scan_photos
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required

def gallery_view(request, folder=""):
    root = Path(settings.MEDIA_ROOT) / "gallery"
    current = root / folder

    if not current.exists() or not current.is_dir():
        raise Http404("Папка не найдена")

    folders = []
    photos = []

    for item in current.iterdir():
        if item.is_dir():
            folders.append(item.name)
        elif item.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            rel = item.relative_to(root).as_posix()
            photos.append(settings.MEDIA_URL + "gallery/" + rel)

    return render(request, "gallery/gallery.html", {
        "folders": folders,
        "photos": photos,
        "current": folder,
    })

def photos_json(request):
    root = Path(settings.MEDIA_ROOT) / "gallery"

    def build_tree(path):
        return {
            "name": path.name,
            "type": "folder" if path.is_dir() else "file",
            "children": [
                build_tree(p)
                for p in path.iterdir()
                if p.is_dir() or p.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp")
            ] if path.is_dir() else None
        }

    return JsonResponse(build_tree(root), safe=False)

def home(request):
    return render(request, "gallery/home.html")
