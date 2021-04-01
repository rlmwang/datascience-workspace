from pathlib import Path

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
