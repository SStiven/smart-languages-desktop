from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaDevices,
    QMediaPlayer,
)
from PySide6.QtCore import QUrl
from PySide6.QtCore import QEventLoop, QTimer


class QAudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        media_devices = QMediaDevices()
        audio_output_device = media_devices.defaultAudioOutput()
        print(audio_output_device.description())

        self.audio_output.setDevice(audio_output_device)
        self.audio_output.setVolume(60)

        self.player.setAudioOutput(self.audio_output)

        self.player.mediaStatusChanged.connect(self.handle_media_state_change)
        self.player.errorOccurred.connect(self.handle_error)

    def play(self, path: str):
        qurl = QUrl.fromLocalFile(path)
        self.player.setSource(qurl)
        if self.player.hasAudio():
            self.player.play()
            self._wait_for_playback_to_finish()

    def handle_media_state_change(self, state):
        print(f"Player state changed: {state}")

    def handle_error(self, error, error_string):
        print(f"Player error occurred: {error} - {error_string}")

    def _wait_for_playback_to_finish(self):
        loop = QEventLoop()
        timer = QTimer()

        def on_state_changed(state):
            if state == QMediaPlayer.PlaybackState.StoppedState:
                timer.singleShot(100, loop.quit)

        self.player.playbackStateChanged.connect(on_state_changed)

        loop.exec_()
