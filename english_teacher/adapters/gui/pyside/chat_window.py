import asyncio
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTextBrowser,
    QTextEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
)
from PySide6.QtCore import QEvent, Qt

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
        self.chat_area = QTextBrowser()
        self.chat_area.setOpenExternalLinks(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.rooms_list)
        hbox.addWidget(self.chat_area)
        main_layout.addLayout(hbox)

        self.message_input = QTextEdit()
        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        self.send_button.clicked.connect(
            lambda: asyncio.create_task(self.send_message())
        )

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

    def build_exchange_html(self, message, response):
        html = f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="text-align: right;"  padding: 5px; border-radius: 7px; word-wrap: break-word;">
                <span style="background-color: #DCF8C6;">
                    {message}
                </span>
            </div>
        </div>
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="text-align: left;">
                <span style="background-color: #ECE5DD; padding: 5px; border-radius: 7px; word-wrap: break-word;">
                    {response}
                </span>
            </div>
        </div>
        """
        return html

    async def send_message(self):
        message = self.message_input.toPlainText().strip()
        if message is None or len(message) == 0:
            return
        self.message_input.clear()
        chat_by_text_service = ChatByText()
        response = await chat_by_text_service.execute(message)
        self.chat_area.insertHtml(self.build_exchange_html(message, response))
        self.chat_area.ensureCursorVisible()
