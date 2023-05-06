import asyncio
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QScrollArea,
    QSplitter,
)
from english_teacher.adapters.external_services.text_to_speech.polly.polly_client import (
    PollyClient,
)
from english_teacher.adapters.gui.pyside.audio_player import QAudioPlayer
from english_teacher.adapters.gui.pyside.audio_recorder import AudioRecorder
from english_teacher.adapters.persistence.filesystem.filesystem_audio_repository import (
    FileSystemAudioRepository,
)


from english_teacher.application.chat_by_text import ChatByText


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Classroom")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.rooms_list = QListWidget()
        self.rooms_list.setMidLineWidth(100)

        self.chat_area = QWidget()
        self.chat_area_layout = QVBoxLayout()
        self.chat_area.setLayout(self.chat_area_layout)

        self.chat_area.minimumSizeHint()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_area)

        self.message_input = QTextEdit()
        self.send_button = QPushButton("Send")

        self.record_button = QPushButton("Record")
        self.record_button.setCheckable(True)
        self.record_button.toggled.connect(self.toggle_recording)
        self.audio_recorder = None

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.record_button)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(self.scroll_area)
        vertical_splitter.addWidget(input_widget)

        horizontal_splitter = QSplitter(Qt.Horizontal)
        horizontal_splitter.addWidget(self.rooms_list)
        horizontal_splitter.addWidget(vertical_splitter)
        main_layout.addWidget(horizontal_splitter)

        self.send_button.clicked.connect(
            lambda: asyncio.create_task(self.send_message())
        )

        self.audio_player = QAudioPlayer()

        self.message_input.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                if event.modifiers() == Qt.ShiftModifier:
                    self.message_input.insertPlainText("\n")
                else:
                    asyncio.create_task(self.send_message())
                return True
        return super().eventFilter(obj, event)

    def showEvent(self, event: QEvent):
        if not event.spontaneous():
            asyncio.create_task(self.populate_rooms())

    async def populate_rooms(self):
        room_names = ["Simple present", "Simple past"]
        await asyncio.sleep(0)
        self.rooms_list.addItems(room_names)

    def toggle_recording(self, checked):
        if checked:
            if self.audio_recorder is None:
                self.audio_recorder = AudioRecorder()
            self.record_button.setText("Stop")
            self.audio_recorder.record()
        else:
            self.audio_recorder.stop()
            self.record_button.setText("Record")

    def add_exchange(self, message, response):
        message_label = QLabel()
        message_label.setWordWrap(True)
        message_label.setTextFormat(Qt.RichText)
        message_label.setMaximumWidth(self.scroll_area.width() * 0.7)
        message_label.setStyleSheet(
            "QLabel { padding: 5px; border-radius: 7px; background-color: #DCF8C6; }"
        )
        message_label.setAlignment(Qt.AlignRight)
        message_label.setText(message)
        self.chat_area_layout.addWidget(message_label)

        response_label = QLabel()
        response_label.setWordWrap(True)
        response_label.setTextFormat(Qt.RichText)
        response_label.setMaximumWidth(self.scroll_area.width() * 0.7)
        response_label.setStyleSheet(
            "QLabel { padding: 5px; border-radius: 7px; background-color: #ECE5DD; }"
        )
        response_label.setAlignment(Qt.AlignLeft)
        response_label.setText(response)
        self.chat_area_layout.addWidget(response_label)

        self.scroll_area.ensureWidgetVisible(response_label)

    async def send_message(self):
        message = self.message_input.toPlainText().strip()
        if message is None or len(message) == 0:
            return
        self.message_input.clear()
        chat_by_text_service = ChatByText()
        response = await chat_by_text_service.execute(message)
        self.add_exchange(message, response)
        text_to_speech_client = PollyClient()
        output_format = "mp3"
        audio_bytes = text_to_speech_client.convert_text_to_audio_bytes(
            response, output_format
        )
        audio_repo = FileSystemAudioRepository()
        file_path = audio_repo.add(audio_bytes, output_format)
        self.audio_player.play(file_path)
