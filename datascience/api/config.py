import os
from pathlib import Path

SHARE_FOLDER = "share"
INPUTS_FOLDER = os.path.join(SHARE_FOLDER, "inputs")
OUTPUT_FOLDER = os.path.join(SHARE_FOLDER, "output")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp3"}

Path(SHARE_FOLDER).mkdir(exist_ok=True)
Path(INPUTS_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
