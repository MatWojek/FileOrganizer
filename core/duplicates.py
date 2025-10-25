#!/usr/bin/python3

import os
import hashlib
from PIL import Image
import cv2

# TODO: 
# Collect information about files:
# - the absolute path 
# - metadata 
# - file hash

# TODO:
# Comparison files 
# - comparison name: delete files with identicaly name in the same folder
# - comparison contents: use a hash MD5 or SHA256 to detect indenticaly content
# - image: Pillow, OpenCV
# - pdf: PyPDF2, pdfplumber
# - pydub, mutagen 

# TODO: 
# Duplicate handling
# - delete duplicates 
# - move to another folder, in case of error
# - save logs with information of deleted files 

# TODO: 
# Optimalization 
# - batch processing: proces files in batches to save memory
# - multithreading

# TODO: 
# Important library:
# - hashing: hashlib
# - images: Pillow, OpenCV
# - videos: opencv, ffmpeg-python 
# - pdf: PyPDF2, pdfplumber 
# - mp3: pydub, mutagen 
# - recursion searching folder: os, pathlib

class IndentifyDuplicates:

    def calculate_hash(filepath):
        """ Calculate the file hash. """
        hash_func = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def find_duplicates(directory):
        """ Find the duplicates in folder. """
        files = {}
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                file_hash = calculate_hash(filepath)
                if file_hash in files:
                    print(f"Duplikat: {filepath} i {files[file_hash]}")
                else:
                    files[file_hash] = filepath

    find_duplicates("/path/to/folder")