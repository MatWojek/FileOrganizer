#!/usr/bin/python3

import os
import sys

from PySide6.QtWidgets import (
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
    QHBoxLayout,
    QComboBox,
    QInputDialog
)

from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt, QDir, qInstallMessageHandler

from PySide6.QtGui import QPalette, QBrush, QPixmap

from core.file_sorter import FileSorter
from core.convert import Convert

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
        self.tree.setColumnWidth(0, 300) 

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

        conversion_button = QPushButton("Convert")
        conversion_button.clicked.connect(self.on_conversion_file)

        # Later add the select box where we choose what type of convertion to use "png -> jpg, jpg -> png"
        self.conversion_type_dropdown = QComboBox()
        self.conversion_type_dropdown.addItems([".jpg -> .png", ".png -> .jpg", ".png -> .svg", ".svg -> .png"])
        
        # Maybe late there are a "+" button to adding and installing a important module to use 

        add_module_button = QPushButton("+")

        self.buttons_list = [sort_files_button, conversion_button, add_module_button]

        # Add buttons to a layout
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(sort_files_button)
        button_layout.addWidget(conversion_button)
        button_layout.addWidget(add_module_button)
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
                self.on_sort_files()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a valid folder to sort.")
                

    def on_sort_files(self):
        """ Call the FileSorter class and handle errors. """
        if not self.selected_folder: 
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return  
        
        try:
            sorter = FileSorter(self.selected_folder, min_size=1024)
            sorter.sort_files()
            QMessageBox.information(self, "Success", "Files have been sorted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def on_conversion_file(self):
        """ Handle file conversion based on user selection. """
        if not self.selected_folder:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return

        # Get the list of conversion types
        conversion_types = self.conversion_type_dropdown.itemText(0)
        conversion_types = [self.conversion_type_dropdown.itemText(i) for i in range(self.conversion_type_dropdown.count())]

        # Create a message box with the list of options
        conversion_type, ok = QInputDialog.getItem(
            self, 
            "Select Conversion Type", 
            "Choose a conversion type:", 
            conversion_types, 
            0, 
            False
        )

        if not ok or not conversion_type:
            QMessageBox.warning(self, "Warning", "No conversion type selected.")
            return

        try:
            converter = Convert(source_dir=self.selected_folder, conversion_type=conversion_type)
            converter.convert()
            QMessageBox.information(self, "Success", f"Conversion completed: {conversion_type}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
