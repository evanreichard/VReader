import os
import vreader

from . import find_article
from datetime import datetime
from flask import Blueprint, request
from vreader.config import Config


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
    filepath = os.path.join(directory, f"{new_title}.md")

    # Write File
    file = open(filepath, 'w', encoding='utf-8')
    file.write(content)
    file.close()

    return { "title": resp["title"] }
