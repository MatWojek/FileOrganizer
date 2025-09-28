import os
import sys

# Add the parent directory (FileOrganizer) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.gui import FileExplorer

from PySide6.QtCore import qInstallMessageHandler
from PySide6.QtWidgets import QApplication, QMessageBox

def qt_message_handler(mode, context, message):
        if "Permission denied" in message:
            QMessageBox.critical(None, "Permission Error", message)

            if window and hasattr(window, "last_valid_index"):
                window.list_view.setRootIndex(window.last_valid_index)
    

if __name__ == "__main__": 

    app = QApplication(sys.argv)

    qInstallMessageHandler(qt_message_handler)

    # Load and apply stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "../gui/style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"File {qss_path} does not exists!")
    
    size = (1200, 800)

    # Create and show main window
    window = FileExplorer(size)
    window.show()

    # Start the event loop
    app.exec()