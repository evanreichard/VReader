import os
from datetime import datetime
from os import path
from flask import Blueprint, request
from vreader.config import Config
import vreader


bp = Blueprint("v1", __name__, url_prefix="/api/v1")


@bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data:
        return {"error": "Missing Data"}

    video = str(data.get("video"))
    if video == "":
        return {"error": "Missing Data"}

    if len(video) != 11:
        return {"error": "Invalid VideoID"}

    metadata = find_article(video)
    if metadata is not None:
        return {"video": video}

    context = vreader.vman.transcribe_video(video)
    if context is None:
        return {"error": "Unable to Extract Subtitles"}

    resp = vreader.oai.query(context)

    # Get Details
    directory = str(Config.DATA_PATH)
    title = resp.get("title")
    content = resp.get("content")
    date = datetime.strftime(datetime.utcnow(), "%Y%m%d%H%M%S")

    # Derive Filename
    new_title = f"{date}_{video}_{title}"
    filepath = path.join(directory, f"{new_title}.md")

    # Write File
    file = open(filepath, 'w', encoding='utf-8')
    file.write(content)
    file.close()

    return { "title": resp["title"] }


def find_article(id):
    directory = str(Config.DATA_PATH)
    files = os.listdir(directory)

    # Find Filename
    filename = next((x for x in files if x[15:26] == id and x.endswith(".md")), None)
    if filename is None:
        return None

    # Normalize File Info
    return get_article_metadata(filename, directory)


def get_article_metadata(filename, directory):
    return {
        "date": filename[:14],
        "video_id": filename[15:26],
        "title": filename[27:][:-3],
        "filepath": os.path.join(directory, filename)
    }
