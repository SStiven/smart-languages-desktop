class Exchange:
    def __init__(self, message, audio_path):
        self._initial = message
        self._initial_audio_path = audio_path

    def add_response(self, response, audio_path):
        self._response = response
        self._response_audio_path = audio_path
