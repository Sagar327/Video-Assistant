import os
import unittest
from unittest.mock import patch

import yt_dlp

import utils.audio_processor as audio_processor


class AudioProcessorTests(unittest.TestCase):
    def test_download_youtube_audio_uses_cookie_file_from_env(self):
        captured = {}

        class DummyYDL:
            def __init__(self, opts):
                captured["opts"] = opts

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def extract_info(self, url, download=True):
                return {"id": "abc123"}

            def prepare_filename(self, info):
                return "/tmp/sample.webm"

        with patch.dict(os.environ, {"YT_DLP_COOKIES": "cookies.txt"}, clear=False):
            with patch.object(audio_processor.yt_dlp, "YoutubeDL", side_effect=lambda opts: DummyYDL(opts)):
                result = audio_processor.download_youtube_audio("https://www.youtube.com/watch?v=abc123")

        self.assertEqual(captured["opts"]["cookiefile"], "cookies.txt")
        self.assertTrue(result.endswith(".wav"))

    def test_download_youtube_audio_surfaces_bot_check_error(self):
        class DummyYDL:
            def __init__(self, *args, **kwargs):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def extract_info(self, url, download=True):
                raise yt_dlp.utils.DownloadError("Sign in to confirm you're not a bot")

        with patch.object(audio_processor.yt_dlp, "YoutubeDL", side_effect=lambda *args, **kwargs: DummyYDL()):
            with self.assertRaisesRegex(RuntimeError, "cookies"):
                audio_processor.download_youtube_audio("https://www.youtube.com/watch?v=abc123")


if __name__ == "__main__":
    unittest.main()
