# media.py
import os

def load_shows(path):

    def sort_key(name: str):
        name_lower = name.lower()
        if name_lower.startswith("the "):
            return name_lower[4:]  # ignore "the "
        return name_lower

    shows = []
    # sort folder names ignoring "The "
    for name in sorted(os.listdir(path), key=sort_key):
        show_path = os.path.join(path, name)
        if os.path.isdir(show_path):
            thumbnail_path = os.path.join(show_path, "thumbnail.png")
            if not os.path.exists(thumbnail_path):
                continue

            # Also sort episodes normally (no need to ignore The here)
            mp4_files = [
                f for f in sorted(os.listdir(show_path))
                if f.lower().endswith(".mp4")
            ]

            if mp4_files:
                shows.append({
                    "name": name,
                    "path": show_path,
                    "thumbnail": thumbnail_path,
                    "episodes": mp4_files
                })

    return shows

