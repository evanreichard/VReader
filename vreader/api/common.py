import os

from . import get_article_metadata, find_article
from flask import Blueprint
from flask import make_response, render_template, send_from_directory
from html_sanitizer import Sanitizer
from markdown import markdown
from vreader.config import Config


bp = Blueprint("common", __name__)
sanitizer = Sanitizer()


@bp.route("/static/<path:path>")
def static(path):
    return send_from_directory("static", path)


@bp.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")


@bp.route("/", methods=["GET"])
def main_entry():
    # Get Files
    directory = str(Config.DATA_PATH)
    all_files = os.listdir(directory)

    # Sort Files
    markdown_files = [file for file in all_files if file.endswith(".md")]
    markdown_files = sorted(markdown_files, reverse=True)

    # Get Article Metadata
    articles = [get_article_metadata(filename, directory) for filename in markdown_files]

    return make_response(render_template("index.html", articles=articles))


@bp.route("/articles/<id>", methods=["GET"])
def article_item(id):

    if len(id) != 11:
        return make_response(
            render_template("error.html", status=404, message="Invalid Article")
        ), 404

    metadata = find_article(id)
    if not metadata:
        return make_response(
            render_template("error.html", status=404, message="Invalid Article")
        ), 404

    try:
        with open(metadata["filepath"], 'r', encoding='utf-8') as file:
            article_contents = file.read()

        markdown_html = sanitizer.sanitize(markdown(article_contents))

        return make_response(
            render_template("article.html", metadata=metadata, markdown_html=markdown_html)
        )
    except Exception as e:
        return make_response(
            render_template("error.html", status=404, message=e)
        ), 404
