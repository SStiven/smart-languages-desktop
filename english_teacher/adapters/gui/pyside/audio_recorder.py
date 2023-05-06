from PySide6.QtMultimedia import (
    QMediaCaptureSession,
    QAudioInput,
    QMediaRecorder,
    QMediaDevices,
)
from PySide6.QtCore import QUrl


class AudioRecorder:
    def __init__(self, filename="/home/stiven/hola.wav"):
        media_devices = QMediaDevices()
        default_audio_input_device = media_devices.defaultAudioInput()

        self.audio_input = QAudioInput()
        self.audio_input.setDevice(default_audio_input_device)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setAudioInput(self.audio_input)

        self.recorder = QMediaRecorder()
        self.recorder.setQuality(QMediaRecorder.Quality.HighQuality)
        self.recorder.setOutputLocation(QUrl.fromLocalFile(filename))

        self.capture_session.setRecorder(self.recorder)
        self.recorder.recorderStateChanged.connect(self.on_state_changed)
        self.recorder.errorOccurred.connect(self.on_error_occurred)

    def record(self):
        self.capture_session.recorder().record()

    def stop(self):
        self.capture_session.recorder().stop()

    def on_state_changed(self, state):
        print(f"Recorder state changed: {state}")

    def on_error_occurred(self, error, error_string):
        print(f"Recorder error occurred: {error} - {error_string}")
