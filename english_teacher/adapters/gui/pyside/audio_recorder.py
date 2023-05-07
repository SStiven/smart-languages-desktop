import os
from PySide6.QtMultimedia import (
    QMediaCaptureSession,
    QAudioInput,
    QMediaRecorder,
    QMediaDevices,
    QMediaFormat,
)
from PySide6.QtCore import QUrl, QTimer
from datetime import datetime


class AudioRecorder:
    def __init__(self, basedir="/home/stiven/Music/"):
        self.basedir = basedir
        media_devices = QMediaDevices()
        default_audio_input_device = media_devices.defaultAudioInput()

        self.audio_input = QAudioInput()
        self.audio_input.setDevice(default_audio_input_device)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setAudioInput(self.audio_input)

        self.recorder = QMediaRecorder()
        self.recorder.setQuality(QMediaRecorder.Quality.HighQuality)

        media_format = QMediaFormat(QMediaFormat.FileFormat.MP3)
        media_format.setAudioCodec(QMediaFormat.AudioCodec.MP3)
        self.recorder.setMediaFormat(media_format)

        self.capture_session.setRecorder(self.recorder)
        self.recorder.recorderStateChanged.connect(self.on_state_changed)
        self.recorder.errorOccurred.connect(self.on_error_occurred)
        self.filename = ""
        self.callback = None

    def record(self, filename=None):
        if not filename:
            origin = "user"
            self.filename = datetime.now().strftime(f"%Y_%m_%d_T%H_%M_%S_{origin}")

        output_path = os.path.join(self.basedir, self.filename)

        self.recorder.setOutputLocation(QUrl.fromLocalFile(output_path))
        self.capture_session.recorder().record()
        return output_path + ".m4a"

    def stop(self, callback):
        self.callback = callback
        self.capture_session.recorder().stop()

    def on_state_changed(self, state):
        if state == QMediaRecorder.RecorderState.StoppedState:
            self.callback()
            print("StoppedState")

        print(f"Recorder state changed: {state}")

    def on_error_occurred(self, error, error_string):
        print(f"Recorder error occurred: {error} - {error_string}")
