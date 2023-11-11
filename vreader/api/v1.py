import os
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

    metadata = get_article_metadata(video)
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

    # Derive Filename
    new_title = f"{video}_{title}"
    file_path = path.join(directory, f"{new_title}.md")

    # Write File
    file = open(file_path, 'w', encoding='utf-8')
    file.write(content)
    file.close()

    return { "title": resp["title"] }


def get_article_metadata(id):
    directory = str(Config.DATA_PATH)
    files = os.listdir(directory)
    for file_name in files:
        if file_name.startswith(id) and file_name.endswith(".md"):
            file_path = os.path.join(directory, file_name)
            metadata = parse_filename(file_name)
            metadata["filepath"] = file_path
            return metadata
    return None


def parse_filename(filename):
    video_id = filename[:11]
    title = filename[12:][:-3]

    return {
        "video_id": video_id,
        "title": title
    }
