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

from PySide6.QtCore import Qt, QDir, qInstallMessageHandler

from PySide6.QtGui import QPalette, QBrush, QPixmap

from core.file_sorter import sort_files

class FileExplorer(QMainWindow):
    def __init__(self, size: tuple):
        super().__init__()
        self.setWindowTitle("File Organizer")
        
        if not size: 
            size = (1200, 800)
        
        self.resize(*size)

        # Set background image
        background_image_path = os.path.join(os.path.dirname(__file__), "background.jpg")
        if os.path.exists(background_image_path):
              self.set_background_image(background_image_path)
        else:
            print(f"File {background_image_path} does not exists!")

        # File system model 
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Filter out folders with no permissions
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Drives)

        # The last valid folder
        self.last_valid_index = self.model.index(QDir.rootPath())

        # Tree view (folders)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setHeaderHidden(True)  
        self.tree.setColumnWidth(0, 100) 

        # List View (files)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(QDir.rootPath()))

        # after click folder in tree -> change list 
        self.tree.clicked.connect(self.on_tree_clicked)

        # After clicking a folder in list_view -> save selected folder
        self.list_view.clicked.connect(self.on_list_view_clicked)

        # Create buttons
        sort_files_button = QPushButton("Sort Files")
        #sort_files_button.setObjectName("sortFilesButton")
        sort_files_button.clicked.connect(self.on_button_click)

        sort_image_button = QPushButton("Sort Image")
        sort_image_button.clicked.connect(self.on_sort_images)

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
        splitter.setSizes([1000, 1000, 500]) 

        # Set central widget
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

        # Store the currently selected folder from list_view
        self.selected_folder = None

    def on_tree_clicked(self, index):
        """Set new catalog in file list"""
        try:
            path = self.model.filePath(index)
            if not os.access(path, os.R_OK):  # Check if the folder is accessible
                raise PermissionError(f"Permission denied: {path}")
            self.last_valid_index = index  # Save last valid folder
            self.list_view.setRootIndex(self.model.index(path))
        except PermissionError as e:
            QMessageBox.critical(self, "Permission Error", str(e))
            self.tree.setCurrentIndex(self.last_valid_index)  # Revert to last valid folder

    def set_background_image(self, image_path):
        """Set a background image for the main window."""
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(image_path)))
        self.setPalette(palette)

    def on_list_view_clicked(self, index):
        """Save the currently selected folder from list_view."""
        try:
            path = self.model.filePath(index)
            if not os.access(path, os.R_OK):  # Check if the folder is accessible
                raise PermissionError(f"Permission denied: {path}")
            if os.path.isdir(path):  # Ensure it's a folder
                self.selected_folder = path
            else:
                self.selected_folder = None
        except PermissionError as e:
            QMessageBox.critical(self, "Permission Error", str(e))
            self.list_view.setRootIndex(self.last_valid_index)  # Revert to last valid folder

 
    def on_button_click(self):
        """ Handle button click to sort files in the currently selected folder. """
        # Get the currently selected folder from the tree view
        folder = self.selected_folder

        if folder and os.path.isdir(folder):
            try:
                self.on_sort_files(folder)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a valid folder to sort.")
                

    def on_sort_files(self, source_folder):
        """ Call the sort_files function and handle errors. """
        print(f"Sorting files in: {source_folder}")
        
        try: 
                # Call the sort_files function
                sort_files(source_dir=source_folder)
                QMessageBox.information(self, "Success", f"Files have been sorted in: {source_folder}")
 
        except Exception as e:  

                QMessageBox.critical(self, "Error", f"An error occured: {e}")
                self.list_view.setRootIndex(self.last_valid_index)
    
    def on_sort_images(self):
        """ Call the sort_images function and handle errors. """
        pass
    
def qt_message_handler(mode, context, message):
        if "Permission denied" in message:
            QMessageBox.critical(None, "Permission Error", message)

            if window and hasattr(window, "last_valid_index"):
                window.list_view.setRootIndex(window.last_valid_index)
    

if __name__ == "__main__":

    app = QApplication(sys.argv)

    qInstallMessageHandler(qt_message_handler)

    # Load and apply stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
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