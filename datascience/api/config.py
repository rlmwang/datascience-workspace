import os
from pathlib import Path

from flask import Flask

app = Flask(__name__, static_url_path="/static")


app.config["VERSION"] = "0.0.1"
app.config["PROJECT"] = "datascience"
app.config["COMPANY"] = "Company Inc."
app.config["EMAIL"] = "wang.roy@gmail.com"

app.config["GITHUB"] = "https://github.com/rlmwang/datascience"
app.config["WEBSITE"] = "https://github.io/rlmwang/datascience"
app.config["LINKEDIN"] = "https://www.linkedin.com/in/rlmwang/"

SHARE_FOLDER = "share"
INPUTS_FOLDER = os.path.join(SHARE_FOLDER, "inputs")
OUTPUT_FOLDER = os.path.join(SHARE_FOLDER, "output")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp3"}

Path(SHARE_FOLDER).mkdir(exist_ok=True)
Path(INPUTS_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
