import os
from yt_dlp import YoutubeDL
import xml.etree.ElementTree as ET

class VideoManager():
    """Transcribe Videos"""

    def transcribe_video(self, video_id: str):
        URLS = [video_id]

        vid = YoutubeDL({
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "ttml",
            "outtmpl": "transcript"
        })

        vid.download(URLS)
        content = self.convert_ttml_to_plain_text("transcript.en.ttml")
        os.remove("transcript.en.ttml")

        return content


    def convert_ttml_to_plain_text(self, ttml_file_path):
        try:
            # Parse the TTML file
            tree = ET.parse(ttml_file_path)
            root = tree.getroot()

            # Process Text
            plain_text = ""
            for elem in root.iter():
                if elem.text:
                    plain_text += elem.text + " "

            return plain_text.strip()
        except ET.ParseError as e:
            print("[VideoManager] TTML Conversion Error:", e)
            return None
