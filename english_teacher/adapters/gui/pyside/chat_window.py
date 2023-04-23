import asyncio
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
)
from PySide6.QtCore import QEvent

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
        self.rooms_list.setMaximumWidth(200)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.rooms_list)
        hbox.addWidget(self.chat_area)
        main_layout.addLayout(hbox)

        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        self.send_button.clicked.connect(
            lambda: asyncio.create_task(self.send_message())
        )

    def showEvent(self, event: QEvent):
        if not event.spontaneous():
            asyncio.create_task(self.populate_rooms())

    async def populate_rooms(self):
        room_names = ["Simple present", "Simple past"]
        await asyncio.sleep(
            0
        )  # Replace this line with your asynchronous code if needed
        self.rooms_list.addItems(room_names)

    async def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.chat_area.append("You: " + message)
            self.message_input.clear()
            service = ChatByText()
            answer = await service.execute(message)
            self.chat_area.append("Assistant: " + answer)
