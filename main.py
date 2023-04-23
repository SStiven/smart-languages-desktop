import sys
import asyncio
from PySide6.QtWidgets import QApplication
import qasync

from english_teacher.adapters.gui.pyside.chat_window import ChatWindow


async def main():
    chat_window = ChatWindow()
    chat_window.show()

    future = asyncio.Future()
    app.aboutToQuit.connect(future.set_result)
    await future


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
