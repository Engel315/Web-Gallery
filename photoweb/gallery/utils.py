from pathlib import Path
import mimetypes
from django.conf import settings

def scan_photos():
    root = Path(settings.MEDIA_ROOT) / "gallery"
    return _scan(root, root)

def _scan(current: Path, root: Path):
    tree = []

    if not current.exists():
        return tree

    for item in sorted(current.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        if item.is_dir():
            tree.append({
                "type": "folder",
                "name": item.name,
                "children": _scan(item, root)
            })
        else:
            mime, _ = mimetypes.guess_type(item)
            if mime and mime.startswith("image"):
                tree.append({
                    "type": "file",
                    "name": item.name,
                    "url": item.relative_to(root).as_posix()
                })
    return tree
