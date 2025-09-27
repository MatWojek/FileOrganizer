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
    QWidget,
    QFileSystemModel,
    QListView, 
    QSplitter,
    QTreeView, 
    QHBoxLayout
)

from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt, QDir

from PySide6.QtGui import QPalette, QBrush, QPixmap

from core.file_sorter import sort_files

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")

        # Set background image
        self.set_background_image("background.jpg")

        # File system model 
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Tree view (folders)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setHeaderHidden(True)  
        self.tree.setColumnWidth(0, 250) 

        # List View (files)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(QDir.rootPath()))

        # after click folder in tree -> change list 
        self.tree.clicked.connect(self.on_tree_clicked)

        # Create buttons
        sort_files_button = QPushButton("Sort Files")
        sort_files_button.setObjectName("sortFilesButton")
        sort_files_button.clicked.connect(self.on_button_click)

        sort_image_button = QPushButton("Sort Image")

        self.buttons_list = [sort_files_button, sort_image_button]

        # Add buttons to a layout
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(sort_files_button)
        button_layout.addWidget(sort_image_button)
        button_layout.addStretch()  # Add stretch to align buttons at the top
        button_widget.setLayout(button_layout)

        # Splitter (3 panels)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.list_view)
        splitter.addWidget(button_widget)  # Add the button widget
        splitter.setSizes([300, 600, 200]) 

        # Set central widget
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)


    def on_tree_clicked(self, index):
        """Set new catalog in file list"""
        path = self.model.filePath(index)
        self.list_view.setRootIndex(self.model.index(path))

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
 # ustaw nowy katalog w liście plików
        except Exception as e:  

                QMessageBox.critical(self, "Error", f"An error occured: {e}")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Load and apply stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print("Plik style.qss nie został znaleziony!")

    # Create and show main window
    window = FileExplorer()
    window.show()

    # Start the event loop
    app.exec()