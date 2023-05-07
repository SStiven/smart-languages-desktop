import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAISpeechToTextClient:
    def __init__(self):
        self.model = "whisper-1"

    def transcribe(self, file_path: str) -> str:
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return ""

        with open(file_path, "rb") as f:
            transcript = openai.Audio.transcribe(
                model=self.model, file=f, content_type="audio/mpeg"
            )
        return transcript.text
