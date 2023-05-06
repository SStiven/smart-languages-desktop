from datetime import datetime


class FileSystemAudioRepository:
    def __init__(self):
        pass

    def add(self, audio_bytes, format):
        user = "user"
        filename = datetime.now().strftime(f"%Y_%m_%d %H_%M_%S_{user}.{format}")
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        return filename
