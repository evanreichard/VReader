from flask import Blueprint
from flask import make_response, render_template
from html_sanitizer import Sanitizer
from markdown import markdown
from vreader.config import Config
import os

bp = Blueprint("common", __name__)
sanitizer = Sanitizer()

@bp.route("/", methods=["GET"])
def main_entry():

    directory = str(Config.DATA_PATH)

    all_files = os.listdir(directory)
    markdown_files = [file for file in all_files if file.endswith(".md")]
    articles = [parse_filename(file) for file in markdown_files]

    return make_response(render_template("index.html", articles=articles))

@bp.route("/articles/<id>", methods=["GET"])
def article_item(id):

    if len(id) != 11:
        return make_response(render_template("404.html")), 404

    metadata = get_article_metadata(id)
    if not metadata:
        return make_response(render_template("404.html")), 404

    try:
        with open(metadata["filepath"], 'r', encoding='utf-8') as file:
            article_contents = file.read()

        markdown_html = sanitizer.sanitize(markdown(article_contents))

        return make_response(
            render_template("article.html", metadata=metadata, markdown_html=markdown_html)
        )
    except Exception as _:
        return make_response(render_template("404.html")), 404


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
