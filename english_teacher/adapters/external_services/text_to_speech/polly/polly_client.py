import os
import boto3

secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
region = os.environ.get("AWS_REGION")


class PollyClient:
    def __init__(self):
        self.polly = boto3.client(
            "polly",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )

    def convert_text_to_audio_bytes(self, text, output_format="mp3", voice_id="Joanna"):
        response = self.polly.synthesize_speech(
            VoiceId=voice_id, Text=text, OutputFormat=output_format
        )
        audio_bytes = response["AudioStream"].read()
        return audio_bytes
