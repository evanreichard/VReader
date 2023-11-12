import os
from vreader.config import Config

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
