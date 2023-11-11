import click
import signal
import sys
from importlib.metadata import version
from vreader.oai import OpenAIConnector
from vreader.video import VideoManager
from flask import Flask
from flask.cli import FlaskGroup

__version__ = version("vreader")

def signal_handler(sig, frame):
    sys.exit(0)


def create_app():
    global oai, vman

    from vreader.config import Config
    import vreader.api.common as api_common
    import vreader.api.v1 as api_v1

    app = Flask(__name__)
    oai = OpenAIConnector(Config.OPENAI_API_KEY)
    vman = VideoManager()

    app.register_blueprint(api_common.bp)
    app.register_blueprint(api_v1.bp)

    return app


@click.group()
def cli():
    """VReader CLI"""


@cli.group(cls=FlaskGroup, create_app=create_app)
def server():
    """VReader flask server"""

signal.signal(signal.SIGINT, signal_handler)
