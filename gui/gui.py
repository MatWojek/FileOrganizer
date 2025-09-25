import os
import sys

# Add the parent directory (FileOrganizer) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QFileDialog, 
    QMessageBox, 
    QVBoxLayout, 
    QPushButton, 
    QWidget
)

from PySide6.QtGui import QPalette, QBrush, QPixmap

from core.file_sorter import sort_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")

        # Set background image
        self.set_background_image("background.jpg")

        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create and add button
        sort_files_button = QPushButton("Sort Files")
        sort_files_button.clicked.connect(self.on_button_click)
        layout.addWidget(sort_files_button)

        sort_image_button = QPushButton("Sort Image")
        layout.addWidget(sort_image_button)

        # Set layout to central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def set_background_image(self, image_path):
        """Set a background image for the main window."""
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(image_path)))
        self.setPalette(palette)

    def on_button_click(self):
        """Handle button click to select folder and sort files."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            if not os.path.isdir(folder):
                QMessageBox.critical(self, "Error", "The provided path is not a directory!")
                return
            self.on_sort_files(folder)

    def on_sort_files(self, source_folder):
        """Call the sort_files function and handle errors. """
        print(f"Sorting files in: {source_folder}")
        
        try: 
                # Call the sort_files function
                sort_files(source_dir=source_folder)
                QMessageBox.information(self, "Success", f"Files have been sorted in: {source_folder}")

        except Exception as e:  

                QMessageBox.critical(self, "Error", f"An error occured: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start the event loop
    app.exec()